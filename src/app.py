# src/app.py
import sys
import os
# Add the project root to proper path to allow absolute imports of 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
from src.utils.retrievers import load_vector_dbs
from src.core.router import route_query
from src.core.rag_chain import create_rag_chain
from src.core.memory import get_memory
from src.models.slm import get_slm
from src.models.llm import get_llm
from src.utils.web_search import WebFallback
from src.utils.visualizer import display_chart_in_response
from src.utils.conversation import get_conversational_response
from src.config.constants import Mode, DOMAINS
from src.utils.logger import get_logger

logger = get_logger()

st.set_page_config(page_title="Private Financial Advisor", layout="centered")
st.title("Private GenAI Financial Advisor")
st.caption("End-to-end private ")

if "memory" not in st.session_state:
    st.session_state.memory = get_memory()
if "messages" not in st.session_state:
    st.session_state.messages = []

retrievers = load_vector_dbs()
web_fallback = WebFallback()

mode = st.selectbox("Mode", [m.value for m in Mode])
hardcoded_intent = st.selectbox("Hardcoded Domain", [""] + DOMAINS) if mode == "hardcoded" else None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask anything about finance..."):
    start_time = time.time()
    logger.info(f"Received user query: {prompt} in mode {mode}")

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Check for conversational queries first (greetings, identity, etc.)
                conversational_answer = get_conversational_response(prompt)
                if conversational_answer:
                    answer = conversational_answer
                else:
                    docs = route_query(prompt, mode, hardcoded_intent or None, retrievers)

                    if not docs:
                        # No local documents found - use web search
                        answer = web_fallback.search_and_scrape(prompt)
                    else:
                        model = get_slm() if mode != "all_db" else get_llm()
                        chain = create_rag_chain(model, retrievers["all"], st.session_state.memory)
                        
                        # Get chat history from memory (ChatMessageHistory has .messages directly)
                        chat_history = st.session_state.memory.messages
                        
                        result = chain.invoke({"input": prompt, "chat_history": chat_history})
                        answer = result["answer"]
                        
                        # Check if RAG response indicates no relevant context found
                        no_context_phrases = [
                            "does not contain",
                            "no information",
                            "not mentioned",
                            "cannot find",
                            "don't have information",
                            "no relevant",
                            "outside the scope",
                            "not available in"
                        ]
                        
                        # If RAG couldn't answer from context, try web search
                        if any(phrase in answer.lower() for phrase in no_context_phrases):
                            web_answer = web_fallback.search_and_scrape(prompt)
                            if web_answer and "unavailable" not in web_answer.lower():
                                answer = web_answer
                        
                        # Update memory with the new exchange
                        st.session_state.memory.add_user_message(prompt)
                        st.session_state.memory.add_ai_message(answer)

                logger.info(f"Generated answer for query: {prompt}")

            except Exception as e:
                answer = "An error occurred. Please try again."
                logger.error(f"Error processing query {prompt}: {str(e)}")

        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Visualization (dummy data; parse from docs/result in production)
        chart_data = {'dates': ['2025-01-01', '2025-12-13'], 'prices': [100, 150]}  # Replace with real extraction
        display_chart_in_response(prompt, chart_data)

        # Human-in-loop feedback with thumbs up/down
        st.markdown("**Rate the response:**")
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("👍 Good", key=f"good_{len(st.session_state.messages)}"):
                st.success("Thanks for the feedback!")
                logger.info(f"User feedback: POSITIVE for query: {prompt}")
        with col2:
            if st.button("👎 Bad", key=f"bad_{len(st.session_state.messages)}"):
                st.warning("Thanks! We'll improve.")
                logger.info(f"User feedback: NEGATIVE for query: {prompt}")

    end_time = time.time()
    logger.info(f"Query processed in {end_time - start_time:.2f} seconds")