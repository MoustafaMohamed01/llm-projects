import os
import pickle
import faiss
import numpy as np


def build_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Create a FAISS flat index and add all chunk embeddings to it.

    Args:
        embeddings: 2-D float32 array of shape (num_chunks, embedding_dim).

    Returns:
        A populated faiss.IndexFlatL2 object.
    """
    embedding_dim = embeddings.shape[1]       

    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)                       

    print(f"FAISS index built with {index.ntotal} vectors (dim={embedding_dim})")
    return index


def save_index(index: faiss.IndexFlatL2, chunks: list[str], save_dir: str) -> None:
    """
    Persist the FAISS index and the original chunk texts to disk.

    We save the index with FAISS's own format and pickle the chunks list
    separately so we can map search results back to readable text.

    Args:
        index:    The FAISS index to save.
        chunks:   The list of original text chunks (parallel to the index).
        save_dir: Directory where files will be written.
    """
    os.makedirs(save_dir, exist_ok=True)

    index_path  = os.path.join(save_dir, "index.faiss")
    chunks_path = os.path.join(save_dir, "chunks.pkl")

    faiss.write_index(index, index_path)

    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)

    print(f"Index saved to {index_path}")
    print(f"Chunks saved to {chunks_path}")


def load_index(save_dir: str) -> tuple[faiss.IndexFlatL2, list[str]]:
    """
    Load a previously saved FAISS index and its chunk texts from disk.

    Args:
        save_dir: Directory where index.faiss and chunks.pkl are stored.

    Returns:
        (index, chunks) — the FAISS index and the list of text chunks.
    """
    index_path  = os.path.join(save_dir, "index.faiss")
    chunks_path = os.path.join(save_dir, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError(
            f"No saved index found in '{save_dir}'. "
            "Please process a document first."
        )

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    print(f"Loaded FAISS index with {index.ntotal} vectors and {len(chunks)} chunks")
    return index, chunks
