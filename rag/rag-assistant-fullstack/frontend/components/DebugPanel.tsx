"use client";
import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import type { DebugChunk } from "@/lib/api";

interface Props {
  chunks: DebugChunk[];
  retrieval_time: number;
  reranking_time: number;
  generation_time: number;
  total_time: number;
}

export default function DebugPanel(p: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="ml-11 mt-1">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 text-[11px] font-mono text-dim hover:text-muted transition-colors"
      >
        {open ? <ChevronDown size={11} /> : <ChevronRight size={11} />}
        debug · {p.chunks.length} chunks · {p.total_time.toFixed(2)}s
      </button>

      {open && (
        <div className="mt-2 bg-panel border border-border rounded-xl p-4 text-[11px] font-mono overflow-x-auto animate-fade-in">
          {/* Timing row */}
          <div className="flex gap-5 mb-3 text-muted">
            <span>retrieval <span className="text-slate-300">{p.retrieval_time.toFixed(3)}s</span></span>
            <span>reranking <span className="text-slate-300">{p.reranking_time.toFixed(3)}s</span></span>
            <span>generation <span className="text-slate-300">{p.generation_time.toFixed(3)}s</span></span>
            <span>total <span className="text-accent font-semibold">{p.total_time.toFixed(3)}s</span></span>
          </div>

          {/* Chunk table */}
          <table className="w-full text-left">
            <thead>
              <tr className="text-dim border-b border-border">
                <th className="pb-1 pr-4">#</th>
                <th className="pb-1 pr-4">Source</th>
                <th className="pb-1 pr-4">Semantic</th>
                <th className="pb-1 pr-4">BM25</th>
                <th className="pb-1 pr-4">Reranker</th>
                <th className="pb-1">Preview</th>
              </tr>
            </thead>
            <tbody>
              {p.chunks.map((c) => (
                <tr key={c.rank} className="border-b border-border/40 text-muted hover:bg-card/40">
                  <td className="py-1 pr-4 text-dim">{c.rank}</td>
                  <td className="py-1 pr-4 text-accent max-w-[70px] truncate">{c.source}</td>
                  <td className="py-1 pr-4">{c.semantic_score.toFixed(3)}</td>
                  <td className="py-1 pr-4">{c.bm25_score.toFixed(3)}</td>
                  <td className="py-1 pr-4">{c.reranker_score.toFixed(3)}</td>
                  <td className="py-1 text-dim max-w-[200px] truncate">{c.text_preview}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
