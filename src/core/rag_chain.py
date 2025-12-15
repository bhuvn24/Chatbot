# src/core/rag_chain.py
"""
RAG Chain implementation using LCEL (LangChain Expression Language).
Compatible with langchain 0.3+ which removed the chains module.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from src.config.constants import PROMPT_TEMPLATE

def format_docs(docs):
    """Format retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(llm, retriever, memory):
    """
    Creates a RAG chain using LCEL (LangChain Expression Language).
    This is the modern langchain 0.3+ approach without using langchain.chains.
    """
    # Create the QA prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a transparent, privacy-focused financial education assistant.
Use only the retrieved context and chat history to answer.
Never give direct investment advice. Always add: "This is not financial advice. Consult a professional."

Context: {context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    # Build the chain using LCEL
    # 1. Get context from retriever
    # 2. Format it
    # 3. Pass to prompt with chat history
    # 4. Send to LLM
    # 5. Parse output
    
    chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["input"]))
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    
    # Wrap to return dict with "answer" key for compatibility
    def invoke_and_wrap(inputs):
        result = chain.invoke(inputs)
        return {"answer": result}
    
    return RunnableLambda(invoke_and_wrap)