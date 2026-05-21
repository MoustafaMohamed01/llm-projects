import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RetrievalStats:
    
    query: str = ""

    semantic_count: int = 0
    bm25_count: int = 0
    hybrid_count: int = 0
    final_count: int = 0

    retrieval_time: float = 0.0
    reranking_time: float = 0.0
    generation_time: float = 0.0

    chunk_details: list[dict] = field(default_factory=list)

    @property
    def total_time(self) -> float:
        return self.retrieval_time + self.reranking_time + self.generation_time


def build_chunk_details(reranked_results: list[dict]) -> list[dict]:
   
    details = []
    for i, result in enumerate(reranked_results, start=1):
        chunk = result["chunk"]
        details.append(
            {
                "rank": i,
                "source": chunk.get("source", "unknown"),
                "chunk_id": chunk.get("chunk_id", "?"),
                "text_preview": chunk["text"][:120] + "..." if len(chunk["text"]) > 120 else chunk["text"],
                "semantic_score": round(result.get("semantic_score") or 0.0, 4),
                "bm25_score": round(result.get("bm25_score") or 0.0, 4),
                "rrf_score": round(result.get("rrf_score") or 0.0, 6),
                "reranker_score": round(result.get("reranker_score") or 0.0, 4),
            }
        )
    return details


def format_debug_markdown(stats: RetrievalStats) -> str:
  
    lines = []

    lines.append("### Retrieval Debug Panel")
    lines.append(f"**Query:** `{stats.query}`\n")

    lines.append("####  Timing")
    lines.append(f"| Stage | Time |")
    lines.append(f"|-------|------|")
    lines.append(f"| Retrieval (Semantic + BM25 + RRF) | {stats.retrieval_time:.3f}s |")
    lines.append(f"| Reranking (CrossEncoder) | {stats.reranking_time:.3f}s |")
    lines.append(f"| Generation (Gemini) | {stats.generation_time:.3f}s |")
    lines.append(f"| **Total** | **{stats.total_time:.3f}s** |")
    lines.append("")

    lines.append("#### Retrieval Counts")
    lines.append(f"| Retriever | Count |")
    lines.append(f"|-----------|-------|")
    lines.append(f"| Semantic (FAISS) candidates | {stats.semantic_count} |")
    lines.append(f"| BM25 candidates | {stats.bm25_count} |")
    lines.append(f"| After hybrid fusion | {stats.hybrid_count} |")
    lines.append(f"| **Final chunks sent to Gemini** | **{stats.final_count}** |")
    lines.append("")

    if stats.chunk_details:
        lines.append("#### Final Chunks (after reranking)")
        lines.append("| Rank | Source | Semantic | BM25 | RRF | Reranker | Preview |")
        lines.append("|------|--------|----------|------|-----|----------|---------|")

        for d in stats.chunk_details:
            sem = f"{d['semantic_score']:.3f}" if d["semantic_score"] else "—"
            bm25 = f"{d['bm25_score']:.3f}" if d["bm25_score"] else "—"
            rrf = f"{d['rrf_score']:.5f}"
            rer = f"{d['reranker_score']:.3f}" if d["reranker_score"] else "—"
            preview = d["text_preview"].replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| {d['rank']} | {d['source']} | {sem} | {bm25} | {rrf} | {rer} | {preview} |"
            )

    return "\n".join(lines)
