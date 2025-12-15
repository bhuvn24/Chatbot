# src/core/router.py
from src.config.constants import LOCAL_DOMAINS
from src.utils.classifiers import classify_intent

def route_query(query: str, mode: str, hardcoded_intent: str | None, retrievers: dict):
    docs = []
    intents = []

    if mode == "hardcoded" and hardcoded_intent:
        intents = [hardcoded_intent]
    elif mode == "classifier":
        intents = classify_intent(query)
    else:  # all_db
        intents = LOCAL_DOMAINS
        docs.extend(retrievers["wiki"].invoke(query))
        docs.extend(retrievers["arxiv"].invoke(query))

    for intent in intents:
        if intent in retrievers:  # Check if DB exists for intent
            docs.extend(retrievers[intent].invoke(query))

    # Deduplicate docs
    return list({d.page_content: d for d in docs}.values())