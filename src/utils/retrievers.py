# src/utils/retrievers.py
"""
Vector database loading utilities.
Loads pre-built FAISS indexes from disk, or builds in-memory as fallback.
"""
import json
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.utils.embeddings import DPEmbeddings
from src.config.settings import Settings
from langchain_community.retrievers import WikipediaRetriever, ArxivRetriever

import streamlit as st

# Path to persisted FAISS indexes
FAISS_INDEX_DIR = Path(__file__).parent.parent.parent / "data" / "faiss_indexes"


def load_json_documents(file_path: str, content_key: str = "markdown"):
    """Load documents from a JSON file."""
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


def load_faiss_index(name: str, embeddings) -> FAISS | None:
    """Load a FAISS index from disk if it exists."""
    index_path = FAISS_INDEX_DIR / name
    if index_path.exists():
        try:
            return FAISS.load_local(
                str(index_path), 
                embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            st.warning(f"Failed to load index '{name}': {e}")
    return None


@st.cache_resource
def load_vector_dbs():
    """
    Load vector databases. Tries to load pre-built indexes from disk first.
    If not available, builds them in-memory (slower).
    """
    embeddings = DPEmbeddings()
    dbs = {}
    
    # Check if indexes exist
    indexes_exist = (FAISS_INDEX_DIR / "all").exists()
    
    if indexes_exist:
        st.info("Loading pre-built FAISS indexes...")
        
        # Load individual domain indexes
        for name in ["investments", "terms", "economic_government", "banking_loans_payments", "currency_crypto"]:
            vs = load_faiss_index(name, embeddings)
            if vs:
                dbs[name] = vs.as_retriever(search_kwargs={"k": 5})
        
        # Load combined index
        all_vs = load_faiss_index("all", embeddings)
        if all_vs:
            dbs["all"] = all_vs.as_retriever(search_kwargs={"k": 8})
        
        st.success(f"Loaded {len(dbs)} indexes from disk.")
    else:
        st.warning("No pre-built indexes found. Building in-memory (run 'python scripts/ingest.py' for faster startup)...")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=Settings.CHUNK_SIZE, 
            chunk_overlap=Settings.CHUNK_OVERLAP
        )
        all_docs = []
        
        # Build each index in memory
        datasets = [
            ("investments", Settings.DATASET_DIR / "investing" / "investing.json", "file", "markdown"),
            ("terms", Settings.DATASET_DIR / "terms", "directory", "markdown"),
            ("economic_government", Settings.DATASET_DIR / "economic_government" / "economic_government.json", "file", "markdown"),
            ("banking_loans_payments", Settings.DATASET_DIR / "banking_loans_payments" / "banking_loans_payments.json", "file", "content"),
            ("currency_crypto", Settings.DATASET_DIR / "currency_crypto" / "currency_crypto.json", "file", "markdown"),
        ]
        
        for name, path, dtype, content_key in datasets:
            if dtype == "file":
                raw_docs = load_json_documents(str(path), content_key)
            else:
                raw_docs = load_directory_json_documents(str(path), content_key)
            
            docs = splitter.split_documents(raw_docs)
            if docs:
                dbs[name] = FAISS.from_documents(docs, embeddings).as_retriever(search_kwargs={"k": 5})
                all_docs.extend(docs)
        
        if all_docs:
            dbs["all"] = FAISS.from_documents(all_docs, embeddings).as_retriever(search_kwargs={"k": 8})
    
    # External retrievers (always available)
    dbs["wiki"] = WikipediaRetriever()
    dbs["arxiv"] = ArxivRetriever()
    
    return dbs