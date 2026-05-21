import { Zap, Database, Brain, GitMerge, MessageSquare, BarChart2 } from "lucide-react";

const pipeline = [
  { n: "1", title: "Upload",    desc: "PDF or TXT → text extracted" },
  { n: "2", title: "Chunk",     desc: "Sliding window with overlap" },
  { n: "3", title: "Embed",     desc: "all-MiniLM-L6-v2 bi-encoder" },
  { n: "4", title: "Index",     desc: "FAISS + BM25 built in parallel" },
  { n: "5", title: "Query",     desc: "Question embedded to vector" },
  { n: "6", title: "Retrieve",  desc: "Semantic + keyword → RRF fusion" },
  { n: "7", title: "Rerank",    desc: "CrossEncoder scores each chunk" },
  { n: "8", title: "Generate",  desc: "Gemini answers from top chunks" },
];

const features = [
  { icon: GitMerge,     title: "Hybrid Search",   desc: "FAISS semantic search + BM25 keyword search fused with Reciprocal Rank Fusion. Gets exact matches AND semantic similarity." },
  { icon: Brain,        title: "CrossEncoder",     desc: "Two-stage pipeline: fast bi-encoder retrieval → precise cross-encoder reranking. Better accuracy than embedding similarity alone." },
  { icon: Database,     title: "FAISS",            desc: "Facebook AI Similarity Search. Sub-millisecond nearest-neighbor lookup across all document chunks using cosine similarity." },
  { icon: Zap,          title: "Gemini 2.5 Flash", desc: "Fast, capable LLM that generates grounded answers strictly from retrieved context. Low hallucination." },
  { icon: MessageSquare,title: "Memory",           desc: "Sliding window of recent exchanges for natural follow-up questions. Sent to Gemini as conversation context." },
  { icon: BarChart2,    title: "Debug Panel",      desc: "Toggle in Chat to inspect per-chunk scores (semantic, BM25, reranker) and timing for every query." },
];

const stack = [
  { label: "Frontend",   items: ["Next.js 14", "React 18", "Tailwind CSS", "TypeScript"] },
  { label: "Backend",    items: ["FastAPI", "Python 3.11+", "Uvicorn"] },
  { label: "Retrieval",  items: ["FAISS CPU", "rank-bm25", "RRF Fusion"] },
  { label: "Reranking",  items: ["CrossEncoder", "ms-marco-MiniLM-L-6-v2"] },
  { label: "Embeddings", items: ["Sentence Transformers", "all-MiniLM-L6-v2"] },
  { label: "LLM",        items: ["Gemini 2.5 Flash", "google-generativeai"] },
];

export default function AboutPage() {
  return (
    <div className="h-screen overflow-y-auto px-6 py-8">
      <div className="max-w-2xl mx-auto space-y-10">

        {/* Hero */}
        <div className="text-center">
          <span className="inline-flex items-center gap-1.5 bg-accent/10 border border-accent/20 rounded-full px-3 py-1 text-accent text-xs font-mono mb-4">
            <Zap size={11} /> Advanced RAG System
          </span>
          <h1 className="text-2xl font-bold text-slate-100">How it works</h1>
          <p className="text-muted text-sm mt-2 leading-relaxed max-w-md mx-auto">
            Full-stack AI document chat using hybrid retrieval — combining semantic search, keyword matching, and neural reranking for accurate, grounded answers.
          </p>
        </div>

        {/* Pipeline */}
        <section>
          <h2 className="text-sm font-semibold text-slate-100 uppercase tracking-wider mb-3">Pipeline</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {pipeline.map(({ n, title, desc }) => (
              <div key={n} className="bg-card border border-border rounded-xl p-3.5">
                <div className="w-6 h-6 rounded-lg bg-accent/15 border border-accent/20 flex items-center justify-center mb-2">
                  <span className="text-accent text-[10px] font-mono font-bold">{n}</span>
                </div>
                <p className="text-slate-200 text-xs font-semibold">{title}</p>
                <p className="text-dim text-[10px] mt-0.5 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Features */}
        <section>
          <h2 className="text-sm font-semibold text-slate-100 uppercase tracking-wider mb-3">Features</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {features.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="bg-card border border-border rounded-xl p-4 hover:border-accent/30 transition-colors">
                <div className="flex items-center gap-2.5 mb-2">
                  <div className="w-7 h-7 rounded-lg bg-accent/10 flex items-center justify-center shrink-0">
                    <Icon size={14} className="text-accent" />
                  </div>
                  <p className="text-slate-200 text-sm font-semibold">{title}</p>
                </div>
                <p className="text-muted text-xs leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Stack */}
        <section>
          <h2 className="text-sm font-semibold text-slate-100 uppercase tracking-wider mb-3">Tech Stack</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {stack.map(({ label, items }) => (
              <div key={label} className="bg-card border border-border rounded-xl p-4">
                <p className="text-dim text-[10px] font-mono uppercase tracking-wider mb-2">{label}</p>
                <ul className="space-y-1">
                  {items.map((i) => <li key={i} className="text-slate-300 text-xs">· {i}</li>)}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <p className="text-center text-dim text-xs font-mono pb-8">
          Built for portfolio · Full-stack AI engineering
        </p>
      </div>
    </div>
  );
}
