# src/config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    
    DATASET_DIR = BASE_DIR / "dataset"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"
    VECTOR_DB_PATH = BASE_DIR / "faiss_index"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    EPSILON_DP = 1.0  # Differential privacy strength (from project PDF)