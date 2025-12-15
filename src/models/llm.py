# src/models/llm.py
from langchain_groq import ChatGroq
from src.config.settings import Settings

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=Settings.GROQ_API_KEY
    )