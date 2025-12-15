# src/utils/embeddings.py
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config.settings import Settings
from src.utils.privacy import add_dp_noise

class DPEmbeddings(HuggingFaceEmbeddings):
    def __init__(self):
        super().__init__(model_name=Settings.EMBEDDING_MODEL)
    
    def embed_documents(self, texts):
        embeds = super().embed_documents(texts)
        return [add_dp_noise(np.array(emb)).tolist() for emb in embeds]
    
    def embed_query(self, text):
        emb = super().embed_query(text)
        return add_dp_noise(np.array(emb)).tolist()