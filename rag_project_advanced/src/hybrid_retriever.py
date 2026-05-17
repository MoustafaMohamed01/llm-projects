import logging
from src.vector_store import semantic_search
from src.bm25_retriever import BM25Retriever

logger = logging.getLogger(__name__)

RRF_K = 60


def reciprocal_rank_fusion(
    semantic_results: list[dict],
    bm25_results: list[dict],
    semantic_weight: float = 1.0,
    bm25_weight: float = 1.0,
) -> list[dict]:
   
    chunk_scores: dict[int, dict] = {}

    for rank, result in enumerate(semantic_results, start=1):
        chunk_id = result["chunk"]["chunk_id"]
        rrf_contribution = semantic_weight / (RRF_K + rank)

        if chunk_id not in chunk_scores:
            chunk_scores[chunk_id] = {
                "chunk": result["chunk"],
                "rrf_score": 0.0,
                "semantic_score": None,
                "bm25_score": None,
            }

        chunk_scores[chunk_id]["rrf_score"] += rrf_contribution
        chunk_scores[chunk_id]["semantic_score"] = result.get("semantic_score")

    for rank, result in enumerate(bm25_results, start=1):
        chunk_id = result["chunk"]["chunk_id"]
        rrf_contribution = bm25_weight / (RRF_K + rank)

        if chunk_id not in chunk_scores:
            chunk_scores[chunk_id] = {
                "chunk": result["chunk"],
                "rrf_score": 0.0,
                "semantic_score": None,
                "bm25_score": None,
            }

        chunk_scores[chunk_id]["rrf_score"] += rrf_contribution
        chunk_scores[chunk_id]["bm25_score"] = result.get("bm25_score")

    merged = sorted(chunk_scores.values(), key=lambda x: x["rrf_score"], reverse=True)
    return merged


def hybrid_search(
    query: str,
    query_embedding,
    faiss_index,
    chunks: list[dict],
    bm25_retriever: BM25Retriever,
    top_k: int = 10,
    semantic_weight: float = 1.0,
    bm25_weight: float = 1.0,
) -> list[dict]:
    
    semantic_results = semantic_search(
        query_embedding=query_embedding,
        index=faiss_index,
        chunks=chunks,
        top_k=top_k,
    )
    logger.debug(f"Semantic search returned {len(semantic_results)} results.")

    bm25_results = bm25_retriever.search(query=query, top_k=top_k)
    logger.debug(f"BM25 search returned {len(bm25_results)} results.")

    merged = reciprocal_rank_fusion(
        semantic_results=semantic_results,
        bm25_results=bm25_results,
        semantic_weight=semantic_weight,
        bm25_weight=bm25_weight,
    )
    logger.debug(f"Hybrid fusion produced {len(merged)} unique candidates.")

    return merged
