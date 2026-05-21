import time
import logging
from typing import List

from fastapi    import APIRouter, HTTPException
from pydantic   import BaseModel

import api.state as state
from src.config          import CANDIDATE_K, FINAL_K, MEMORY_K
from src.embeddings      import embed_query
from src.vector_store    import semantic_search
from src.hybrid_retriever import hybrid_search
from src.reranker        import rerank
from src.memory          import Message, format_history_for_prompt, get_recent_history
from src.generator       import generate_answer
from src.evaluation      import build_chunk_details

logger = logging.getLogger(__name__)
router = APIRouter()


class HistoryMsg(BaseModel):
    role: str     
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[HistoryMsg] = []


@router.post("/chat")
def chat(req: ChatRequest):
    if not state.is_ready():
        raise HTTPException(
            status_code=503,
            detail="No documents indexed yet. Please upload files first."
        )

    q_emb = embed_query(req.message)

    t0 = time.time()
    results = hybrid_search(
        query=req.message,
        query_embedding=q_emb,
        faiss_index=state.faiss_index,
        chunks=state.chunks,
        bm25_retriever=state.bm25,
        top_k=CANDIDATE_K,
    )
    retrieval_time = round(time.time() - t0, 3)

    t1 = time.time()
    reranked = rerank(query=req.message, candidates=results, top_k=FINAL_K)
    reranking_time = round(time.time() - t1, 3)

    memory_msgs = [Message(role=m.role, content=m.content) for m in req.history]
    recent      = get_recent_history(memory_msgs, max_exchanges=MEMORY_K)
    history_str = format_history_for_prompt(recent)

    answer, gen_time = generate_answer(
        context_chunks=reranked,
        history_text=history_str,
        question=req.message,
    )

    debug_chunks = build_chunk_details(reranked)
    sources = list(dict.fromkeys(d["source"] for d in debug_chunks))

    return {
        "answer": answer,
        "sources": sources,
        "debug": {
            "chunks": debug_chunks,
            "retrieval_time": retrieval_time,
            "reranking_time": reranking_time,
            "generation_time": round(gen_time, 3),
            "total_time": round(retrieval_time + reranking_time + gen_time, 3),
        },
    }
