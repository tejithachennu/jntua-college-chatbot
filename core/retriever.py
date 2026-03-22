"""
retriever.py
Searches the FAISS index for the most relevant chunks for a given query.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TOP_K, CONFIDENCE_THRESHOLD
from core.embedder import embed_query, load_index


def retrieve(query: str) -> tuple[list[dict], float]:
    """
    Returns (list of relevant chunks, best confidence score).
    Each chunk: {text, source, score}
    """
    index, chunks = load_index()
    if index is None or not chunks:
        return [], 0.0

    query_vec = embed_query(query)
    scores, indices = index.search(query_vec, TOP_K)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = chunks[idx].copy()
        chunk["score"] = float(score)
        results.append(chunk)

    best_score = results[0]["score"] if results else 0.0
    is_confident = best_score >= CONFIDENCE_THRESHOLD

    return results if is_confident else results, best_score
