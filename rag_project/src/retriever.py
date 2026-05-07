import faiss
import numpy as np
from src.embeddings import embed_query


def retrieve(
    query: str,
    index: faiss.IndexFlatL2,
    chunks: list[str],
    top_k: int = 3,
) -> list[str]:
    """
    Retrieve the top-k chunks most relevant to the query.

    Args:
        query:   The user's question (plain text).
        index:   A populated FAISS index.
        chunks:  The list of original text chunks parallel to the index.
        top_k:   How many chunks to return (default 3).

    Returns:
        A list of up to top_k text strings, ordered by relevance
        (most relevant first).
    """
    query_vector = embed_query(query)

    distances, indices = index.search(query_vector, top_k)

    retrieved_chunks = []
    for idx in indices[0]:
        if idx == -1:
            continue
        retrieved_chunks.append(chunks[idx])

    return retrieved_chunks
