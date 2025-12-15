# src/models/slm.py
from langchain_groq import ChatGroq
from src.config.settings import Settings

def get_slm():
    return ChatGroq(
        model="llama-3.1-8b-instant",  # Small/fast model for quick responses
        temperature=0.7,
        groq_api_key=Settings.GROQ_API_KEY
    )