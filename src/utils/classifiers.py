# src/utils/classifiers.py
from transformers import pipeline
from src.config.constants import DOMAINS

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_intent(query: str, threshold: float = 0.3):
    result = classifier(query, candidate_labels=DOMAINS)
    return [
        label for label, score in zip(result["labels"], result["scores"])
        if score > threshold
    ]