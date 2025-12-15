# src/config/constants.py
from enum import Enum

class Mode(Enum):
    HARDCODED = "hardcoded"
    CLASSIFIER = "classifier"
    ALL_DB = "all_db"

DOMAINS = [
    "stocks_investments", "economic_government",
    "banking_loans_payments", "currency_crypto"
]

LOCAL_DOMAINS = ["investments", "terms", "economic_government", "banking_loans_payments", "currency_crypto"]

PROMPT_TEMPLATE = """
You are a transparent, privacy-focused financial education assistant (as per project abstract).
Use only the retrieved context and chat history to answer.
Personalize insights based on user's past queries (e.g., if they asked about stocks before, relate to markets).
Never give direct investment advice. Always add: "This is not financial advice. Consult a professional."

Context: {context}
Chat History: {chat_history}
Question: {question}

Answer clearly, factually, and include sources when possible. For calculations, show steps.
"""