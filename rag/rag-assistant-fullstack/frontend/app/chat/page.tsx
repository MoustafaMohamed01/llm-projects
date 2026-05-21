"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Trash2, Bug } from "lucide-react";
import clsx from "clsx";
import ChatBubble, { TypingDots } from "@/components/ChatBubble";
import DebugPanel from "@/components/DebugPanel";
import { chat, type Message, type DebugChunk } from "@/lib/api";

interface Msg extends Message {
  id: number;
  sources?: string[];
  debug?: {
    chunks: DebugChunk[];
    retrieval_time: number;
    reranking_time: number;
    generation_time: number;
    total_time: number;
  };
}

let _id = 0;
const nextId = () => ++_id;

const STARTERS = [
  "What are the main topics covered?",
  "Summarize the key points",
  "What does this document say about...",
];

export default function ChatPage() {
  const [msgs, setMsgs]       = useState<Msg[]>([]);
  const [input, setInput]     = useState("");
  const [loading, setLoading] = useState(false);
  const [debug, setDebug]     = useState(false);
  const [error, setError]     = useState("");
  const bottomRef             = useRef<HTMLDivElement>(null);
  const taRef                 = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, loading]);

  useEffect(() => {
    const ta = taRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 150) + "px";
  }, [input]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setError("");

    const userMsg: Msg = { id: nextId(), role: "user", content: text };
    setMsgs((prev) => [...prev, userMsg]);
    setLoading(true);

    const history: Message[] = msgs.slice(-8).map((m) => ({ role: m.role, content: m.content }));

    try {
      const res = await chat(text, history);
      const aiMsg: Msg = {
        id: nextId(),
        role: "assistant",
        content: res.answer,
        sources: res.sources,
        debug: res.debug,
      };
      setMsgs((prev) => [...prev, aiMsg]);
    } catch (e: any) {
      setError(e.message ?? "Something went wrong. Is the backend running on port 8000?");
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  }

  return (
    <div className="flex flex-col h-screen">

      {/* ── Top bar ── */}
      <header className="shrink-0 flex items-center justify-between px-6 py-3 border-b border-border bg-panel/70 backdrop-blur">
        <div>
          <h1 className="font-semibold text-slate-100 text-sm">Document Chat</h1>
          <p className="text-[11px] font-mono text-muted">Hybrid Search · CrossEncoder · Gemini 2.5 Flash</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setDebug(!debug)}
            className={clsx(
              "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs border transition-all",
              debug ? "bg-accent/10 text-accent border-accent/25" : "bg-card text-muted border-border hover:text-accent hover:border-accent/40"
            )}
          >
            <Bug size={12} /> Debug
          </button>
          <button
            onClick={() => { setMsgs([]); setError(""); }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs bg-card text-muted border border-border hover:text-danger hover:border-danger/40 transition-all"
          >
            <Trash2 size={12} /> Clear
          </button>
        </div>
      </header>

      {/* ── Messages ── */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-5">

        {/* Empty state */}
        {msgs.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full gap-5 text-center animate-fade-in">
            <div className="w-14 h-14 rounded-2xl bg-accent/10 border border-accent/20 flex items-center justify-center">
              <Send size={24} className="text-accent" />
            </div>
            <div>
              <h2 className="font-semibold text-slate-100 text-base">Chat with your documents</h2>
              <p className="text-muted text-sm mt-1.5 max-w-xs leading-relaxed">
                Upload PDFs or text files first, then ask anything. Powered by hybrid retrieval + reranking.
              </p>
            </div>
            {/* Starter suggestions */}
            <div className="flex flex-wrap gap-2 justify-center mt-1">
              {STARTERS.map((q) => (
                <button
                  key={q}
                  onClick={() => setInput(q)}
                  className="text-xs px-3 py-1.5 rounded-full bg-card border border-border text-muted hover:text-accent hover:border-accent/40 transition-all"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message list */}
        {msgs.map((msg) => (
          <div key={msg.id}>
            <ChatBubble message={msg} />
            {/* Debug panel under each AI message */}
            {debug && msg.role === "assistant" && msg.debug && (
              <DebugPanel {...msg.debug} />
            )}
          </div>
        ))}

        {loading && <TypingDots />}

        {error && (
          <div className="max-w-lg mx-auto bg-danger/10 border border-danger/30 rounded-xl px-4 py-3 text-danger text-sm animate-fade-in">
            ⚠️ {error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* ── Input bar ── */}
      <div className="shrink-0 px-4 pb-4 pt-2 border-t border-border bg-surface">
        <div className="max-w-2xl mx-auto">
          <div className={clsx(
            "flex items-end gap-3 bg-input border rounded-2xl px-4 py-3 transition-all",
            "border-border focus-within:border-accent focus-within:shadow-[0_0_0_3px_rgba(91,141,238,0.1)]"
          )}>
            <textarea
              ref={taRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask about your documents…  (Enter to send · Shift+Enter for newline)"
              className="flex-1 bg-transparent resize-none outline-none text-slate-100 placeholder:text-dim text-sm leading-relaxed"
              style={{ maxHeight: 150 }}
            />
            <button
              onClick={send}
              disabled={!input.trim() || loading}
              className={clsx(
                "w-9 h-9 rounded-xl flex items-center justify-center shrink-0 transition-all",
                input.trim() && !loading
                  ? "bg-accent hover:bg-accent-h text-white"
                  : "bg-card text-dim cursor-not-allowed"
              )}
            >
              <Send size={14} />
            </button>
          </div>
          <p className="text-center text-[10px] text-dim font-mono mt-2">
            Answers are grounded in your documents via hybrid search + reranking.
          </p>
        </div>
      </div>
    </div>
  );
}
