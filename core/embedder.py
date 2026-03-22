"""
embedder.py
Generates sentence embeddings and builds/saves/loads a FAISS index.
"""

import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FAISS_DIR, EMBED_MODEL

INDEX_FILE = os.path.join(FAISS_DIR, "index.faiss")
META_FILE = os.path.join(FAISS_DIR, "index.pkl")

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def build_index(chunks: list[dict], progress_callback=None) -> None:
    """
    Embed all chunks and save FAISS index + metadata to disk.
    chunks: list of {text, source}
    """
    model = get_model()
    texts = [c["text"] for c in chunks]

    if progress_callback:
        progress_callback("Generating embeddings...", 0.85)

    print(f"[Embedder] Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
    embeddings = np.array(embeddings, dtype="float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner product = cosine after normalization
    index.add(embeddings)

    os.makedirs(FAISS_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"[Embedder] Index saved. {index.ntotal} vectors stored.")
    if progress_callback:
        progress_callback("Index built successfully!", 1.0)


def load_index():
    """Load FAISS index and metadata from disk."""
    if not os.path.exists(INDEX_FILE):
        return None, None
    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def index_exists() -> bool:
    return os.path.exists(INDEX_FILE) and os.path.exists(META_FILE)


def embed_query(query: str) -> np.ndarray:
    """Embed a single query string."""
    model = get_model()
    vec = model.encode([query], show_progress_bar=False)
    vec = np.array(vec, dtype="float32")
    faiss.normalize_L2(vec)
    return vec
