# src/core/memory.py
"""
Simple chat memory using langchain_community.
Compatible with langchain 0.3+ which removed langchain.memory.
"""
from langchain_community.chat_message_histories import ChatMessageHistory

def get_memory():
    """Returns a simple chat message history for storing conversation."""
    return ChatMessageHistory()