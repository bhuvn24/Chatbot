#!/usr/bin/env python
"""
Data Ingestion Script for Financial Chatbot
============================================
This script builds FAISS vector indexes from the dataset JSON files
and saves them to disk for fast loading by the application.

Usage: python scripts/ingest.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.utils.embeddings import DPEmbeddings
from src.config.settings import Settings

# Where to save FAISS indexes
FAISS_INDEX_DIR = Path(__file__).parent.parent / "data" / "faiss_indexes"


def load_json_documents(file_path: str, content_key: str = "markdown"):
    """Load documents from a JSON file."""
    print(f"  Loading: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict) and content_key in data:
        return [Document(page_content=data[content_key], metadata={"source": file_path})]
    
    if isinstance(data, list):
        docs = []
        for item in data:
            if isinstance(item, dict):
                content = item.get(content_key) or item.get("content") or str(item)
                docs.append(Document(page_content=content, metadata={"source": file_path}))
        return docs
    
    return [Document(page_content=str(data), metadata={"source": file_path})]


def load_directory_json_documents(dir_path: str, content_key: str = "markdown"):
    """Load all JSON files from a directory."""
    docs = []
    for json_file in Path(dir_path).glob("*.json"):
        docs.extend(load_json_documents(str(json_file), content_key))
    return docs


def build_and_save_index(name: str, docs: list, embeddings, save_dir: Path):
    """Build a FAISS index and save it to disk."""
    print(f"  Building index '{name}' with {len(docs)} documents...")
    
    if not docs:
        print(f"  WARNING: No documents for '{name}', skipping.")
        return None
        
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    index_path = save_dir / name
    vectorstore.save_local(str(index_path))
    print(f"  Saved index to: {index_path}")
    
    return vectorstore


def main():
    print("=" * 60)
    print("Financial Chatbot - Data Ingestion")
    print("=" * 60)
    
    # Create output directory
    FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {FAISS_INDEX_DIR}")
    
    # Initialize embeddings and splitter
    print("\nInitializing embeddings model...")
    embeddings = DPEmbeddings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Settings.CHUNK_SIZE,
        chunk_overlap=Settings.CHUNK_OVERLAP
    )
    
    all_docs = []
    
    # Define datasets to process
    datasets = [
        {
            "name": "investments",
            "path": Settings.DATASET_DIR / "investing" / "investing.json",
            "type": "file",
            "content_key": "markdown"
        },
        {
            "name": "terms",
            "path": Settings.DATASET_DIR / "terms",
            "type": "directory",
            "content_key": "markdown"
        },
        {
            "name": "economic_government",
            "path": Settings.DATASET_DIR / "economic_government" / "economic_government.json",
            "type": "file",
            "content_key": "markdown"
        },
        {
            "name": "banking_loans_payments",
            "path": Settings.DATASET_DIR / "banking_loans_payments" / "banking_loans_payments.json",
            "type": "file",
            "content_key": "content"
        },
        {
            "name": "currency_crypto",
            "path": Settings.DATASET_DIR / "currency_crypto" / "currency_crypto.json",
            "type": "file",
            "content_key": "markdown"
        },
    ]
    
    # Process each dataset
    for dataset in datasets:
        print(f"\n[{dataset['name'].upper()}]")
        
        if dataset["type"] == "file":
            raw_docs = load_json_documents(str(dataset["path"]), dataset["content_key"])
        else:
            raw_docs = load_directory_json_documents(str(dataset["path"]), dataset["content_key"])
        
        # Split documents
        docs = splitter.split_documents(raw_docs)
        print(f"  Split into {len(docs)} chunks")
        
        # Build and save index
        build_and_save_index(dataset["name"], docs, embeddings, FAISS_INDEX_DIR)
        all_docs.extend(docs)
    
    # Build combined "all" index
    print(f"\n[ALL - COMBINED]")
    print(f"  Total documents: {len(all_docs)}")
    build_and_save_index("all", all_docs, embeddings, FAISS_INDEX_DIR)
    
    print("\n" + "=" * 60)
    print("Ingestion complete!")
    print(f"Indexes saved to: {FAISS_INDEX_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
