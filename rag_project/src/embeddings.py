import numpy as np
from sentence_transformers import SentenceTransformer


_MODEL_NAME = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Return the shared SentenceTransformer model (lazy-load)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_chunks(chunks: list[str]) -> np.ndarray:
    """
    Embed a list of text chunks into a 2-D float32 numpy array.

    Args:
        chunks: List of text strings (your document chunks).

    Returns:
        Array of shape (len(chunks), 384) — one row per chunk.
    """
    model = _get_model()
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)
    return embeddings.astype("float32")


def embed_query(query: str) -> np.ndarray:
    """
    Embed a single user query into a 1-D float32 numpy array.

    Args:
        query: The user's question string.

    Returns:
        Array of shape (384,).
    """
    model = _get_model()
    vector = model.encode([query], convert_to_numpy=True)
    return vector.astype("float32")
