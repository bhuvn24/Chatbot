# src/utils/conversation.py
"""
Conversational response handler for basic greetings and identity questions.
Handles queries that don't require RAG or web search.
"""
import re

# Bot identity and capabilities
BOT_NAME = "Private Financial Advisor"
BOT_DESCRIPTION = """I'm a privacy-focused AI financial education assistant. I can help you learn about:

• **Investing** - Stocks, bonds, ETFs, mutual funds
• **Banking** - Loans, payments, credit cards
• **Cryptocurrency** - Bitcoin, blockchain, digital assets
• **Economics** - Government policy, markets, economic indicators
• **Financial Terms** - Definitions and explanations

I use your local data to provide personalized insights while keeping your information private.

**Note:** I provide educational information only. This is not financial advice - please consult a professional for investment decisions."""

# Patterns and responses for conversational queries
CONVERSATIONAL_PATTERNS = [
    # Greetings
    {
        "patterns": [r"^hi\b", r"^hello\b", r"^hey\b", r"^greetings\b", r"^good (morning|afternoon|evening)\b"],
        "response": f"Hello! 👋 I'm your {BOT_NAME}. How can I help you with your financial questions today?"
    },
    # Identity questions
    {
        "patterns": [r"who are you", r"what are you", r"what is your name", r"your name"],
        "response": f"I'm the **{BOT_NAME}**! {BOT_DESCRIPTION}"
    },
    # Capability questions  
    {
        "patterns": [r"what (can|do) you do", r"what are your (capabilities|features)", r"how can you help", r"what can you help"],
        "response": BOT_DESCRIPTION
    },
    # How are you
    {
        "patterns": [r"how are you", r"how('s| is) it going", r"how do you do"],
        "response": "I'm doing great, thank you for asking! Ready to help you with any financial questions. What would you like to learn about today?"
    },
    # Thanks
    {
        "patterns": [r"^thanks?\b", r"^thank you\b", r"^ty\b", r"appreciate"],
        "response": "You're welcome! Feel free to ask if you have more financial questions. 😊"
    },
    # Goodbye
    {
        "patterns": [r"^bye\b", r"^goodbye\b", r"see you", r"take care"],
        "response": "Goodbye! Feel free to come back anytime you have financial questions. Take care! 👋"
    },
    # Help
    {
        "patterns": [r"^help\b", r"^help me\b"],
        "response": f"I'd be happy to help! {BOT_DESCRIPTION}\n\nJust ask me any financial question to get started!"
    },
]


def get_conversational_response(query: str) -> str | None:
    """
    Check if the query is a basic conversational question and return an appropriate response.
    Returns None if the query should be handled by RAG/web search.
    """
    query_lower = query.lower().strip()
    
    for item in CONVERSATIONAL_PATTERNS:
        for pattern in item["patterns"]:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return item["response"]
    
    return None


def is_conversational_query(query: str) -> bool:
    """Check if the query is a conversational question."""
    return get_conversational_response(query) is not None
