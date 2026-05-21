import os
import pickle
import logging
import numpy as np

import faiss

logger = logging.getLogger(__name__)

INDEX_PATH = "faiss_index.bin"
CHUNKS_PATH = "chunks_cache.pkl"


def build_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(embedding_dim)  
    index.add(embeddings.astype("float32"))    
    logger.info(f"FAISS index built with {index.ntotal} vectors (dim={embedding_dim})")
    return index


def save_index(index: faiss.IndexFlatIP, chunks: list[dict],
               index_path: str = INDEX_PATH, chunks_path: str = CHUNKS_PATH):
    
    faiss.write_index(index, index_path)
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)
    logger.info(f"Index saved → {index_path} | Chunks saved → {chunks_path}")


def load_index(index_path: str = INDEX_PATH, chunks_path: str = CHUNKS_PATH):
    
    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        logger.info("No cached index found. Will build from scratch.")
        return None, None

    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    logger.info(f"Loaded cached index with {index.ntotal} vectors and {len(chunks)} chunks.")
    return index, chunks


def semantic_search(
    query_embedding: np.ndarray,
    index: faiss.IndexFlatIP,
    chunks: list[dict],
    top_k: int = 10,
) -> list[dict]:
    
    query_vec = query_embedding.astype("float32")

    scores, indices = index.search(query_vec, min(top_k, index.ntotal))

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx == -1:
            continue
        results.append(
            {
                "chunk": chunks[idx],
                "semantic_score": float(score),
                "rank": rank,
            }
        )

    return results
