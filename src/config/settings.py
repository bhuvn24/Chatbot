# src/config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

def get_secret(key: str, default: str = None) -> str:
    """
    Get secret from Streamlit Cloud secrets or environment variables.
    Streamlit Cloud uses st.secrets, local development uses .env
    """
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    
    # Fall back to environment variables (for local development)
    return os.getenv(key, default)

class Settings:
    GROQ_API_KEY = get_secret("GROQ_API_KEY")
    SERPER_API_KEY = get_secret("SERPER_API_KEY")
    FIRECRAWL_API_KEY = get_secret("FIRECRAWL_API_KEY")
    
    DATASET_DIR = BASE_DIR / "dataset"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"
    VECTOR_DB_PATH = BASE_DIR / "faiss_index"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    EPSILON_DP = 1.0  # Differential privacy strength (from project PDF)