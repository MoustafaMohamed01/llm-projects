import logging

logger = logging.getLogger(__name__)

_reranker_model = None
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def get_reranker():
    
    global _reranker_model
    if _reranker_model is None:
        logger.info(f"Loading reranker model: {RERANKER_MODEL}")
        from sentence_transformers import CrossEncoder
        _reranker_model = CrossEncoder(RERANKER_MODEL)
        logger.info("Reranker model loaded.")
    return _reranker_model


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
) -> list[dict]:
    
    if not candidates:
        return []

    reranker = get_reranker()

    pairs = [(query, candidate["chunk"]["text"]) for candidate in candidates]

    scores = reranker.predict(pairs)

    scored_candidates = []
    for candidate, score in zip(candidates, scores):
        enriched = dict(candidate) 
        enriched["reranker_score"] = float(score)
        scored_candidates.append(enriched)

    scored_candidates.sort(key=lambda x: x["reranker_score"], reverse=True)

    logger.debug(
        f"Reranked {len(candidates)} candidates → returning top {top_k}. "
        f"Top score: {scored_candidates[0]['reranker_score']:.3f}"
    )

    return scored_candidates[:top_k]
