import logging
import numpy as np

logger = logging.getLogger(__name__)

_model = None
MODEL_NAME = "all-MiniLM-L6-v2"


def get_model():
    
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {MODEL_NAME}")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
        logger.info("Embedding model loaded successfully.")
    return _model


def embed_texts(texts: list[str], batch_size: int = 64) -> np.ndarray:
    
    model = get_model()
    show_progress = len(texts) > 10

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
        normalize_embeddings=True,   
    )
    return embeddings


def embed_query(query: str) -> np.ndarray:
    return embed_texts([query])
