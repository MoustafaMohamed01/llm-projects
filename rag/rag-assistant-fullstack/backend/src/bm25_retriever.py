import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def simple_tokenize(text: str) -> list[str]:
   
    tokens = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    return tokens


class BM25Retriever:
    

    def __init__(self, chunks: list[dict]):
        
        from rank_bm25 import BM25Okapi

        self.chunks = chunks

        tokenized_corpus = [simple_tokenize(chunk["text"]) for chunk in chunks]

        self.bm25 = BM25Okapi(tokenized_corpus)

        logger.info(f"BM25 index built over {len(chunks)} chunks.")

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        
        tokenized_query = simple_tokenize(query)

        if not tokenized_query:
            logger.warning("BM25: Empty query after tokenization.")
            return []

        scores = self.bm25.get_scores(tokenized_query)

        import numpy as np
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices):
            score = float(scores[idx])
            if score <= 0.0:
                continue
            results.append(
                {
                    "chunk": self.chunks[idx],
                    "bm25_score": score,
                    "rank": rank,
                }
            )

        return results
