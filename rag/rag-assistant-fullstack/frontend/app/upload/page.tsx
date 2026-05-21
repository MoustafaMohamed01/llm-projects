"use client";
import { useState, useCallback } from "react";
import { Upload, FileText, X, CheckCircle, Loader2, AlertCircle } from "lucide-react";
import clsx from "clsx";
import { upload, type UploadResult } from "@/lib/api";

type State = "idle" | "uploading" | "done" | "error";

export default function UploadPage() {
  const [files, setFiles]   = useState<File[]>([]);
  const [state, setState]   = useState<State>("idle");
  const [result, setResult] = useState<UploadResult | null>(null);
  const [err, setErr]       = useState("");
  const [drag, setDrag]     = useState(false);

  function addFiles(incoming: FileList | null) {
    if (!incoming) return;
    const valid = Array.from(incoming).filter(
      (f) => f.name.endsWith(".pdf") || f.name.endsWith(".txt")
    );
    setFiles((prev) => {
      const names = new Set(prev.map((f) => f.name));
      return [...prev, ...valid.filter((f) => !names.has(f.name))];
    });
  }

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDrag(false);
    addFiles(e.dataTransfer.files);
  }, []);

  async function handleUpload() {
    if (!files.length) return;
    setState("uploading");
    setErr("");
    try {
      const res = await upload(files);
      setResult(res);
      setState("done");
      setFiles([]);
    } catch (e: any) {
      setErr(e.message ?? "Upload failed.");
      setState("error");
    }
  }

  return (
    <div className="h-screen overflow-y-auto px-6 py-8">
      <div className="max-w-xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-xl font-semibold text-slate-100">Upload Documents</h1>
          <p className="text-muted text-sm mt-1">
            Upload PDF or TXT files. They will be chunked, embedded, and indexed for hybrid retrieval.
          </p>
        </div>

        {/* Drop zone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
          onDragLeave={() => setDrag(false)}
          onDrop={onDrop}
          onClick={() => document.getElementById("filein")?.click()}
          className={clsx(
            "rounded-2xl border-2 border-dashed p-10 text-center cursor-pointer transition-all",
            drag ? "border-accent bg-accent/5" : "border-border bg-card hover:border-accent/50 hover:bg-input"
          )}
        >
          <input id="filein" type="file" accept=".pdf,.txt" multiple className="hidden" onChange={(e) => addFiles(e.target.files)} />
          <Upload size={32} className={clsx("mx-auto mb-3", drag ? "text-accent" : "text-muted")} />
          <p className="text-slate-200 font-medium">{drag ? "Drop here" : "Drag & drop or click to browse"}</p>
          <p className="text-muted text-sm mt-1">PDF and TXT · up to 20 MB each</p>
        </div>

        {/* File list */}
        {files.length > 0 && (
          <div className="space-y-2 animate-fade-in">
            {files.map((f) => (
              <div key={f.name} className="flex items-center justify-between bg-card border border-border rounded-xl px-4 py-3">
                <div className="flex items-center gap-3">
                  <FileText size={15} className="text-accent shrink-0" />
                  <div>
                    <p className="text-slate-200 text-sm font-medium">{f.name}</p>
                    <p className="text-muted text-xs">{(f.size / 1024).toFixed(1)} KB</p>
                  </div>
                </div>
                <button onClick={() => setFiles((p) => p.filter((x) => x.name !== f.name))} className="text-dim hover:text-danger transition-colors">
                  <X size={15} />
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Upload button */}
        <button
          onClick={handleUpload}
          disabled={!files.length || state === "uploading"}
          className={clsx(
            "w-full py-3 rounded-xl text-sm font-medium flex items-center justify-center gap-2 transition-all",
            files.length && state !== "uploading"
              ? "bg-accent hover:bg-accent-h text-white"
              : "bg-card text-dim border border-border cursor-not-allowed"
          )}
        >
          {state === "uploading"
            ? <><Loader2 size={15} className="animate-spin" /> Indexing…</>
            : <><Upload size={15} /> Build Index</>}
        </button>

        {/* Success */}
        {state === "done" && result && (
          <div className="bg-success/10 border border-success/30 rounded-2xl p-5 animate-fade-up">
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle size={17} className="text-success" />
              <span className="text-success font-semibold text-sm">Index built successfully</span>
            </div>
            <div className="grid grid-cols-2 gap-3 mb-4">
              {[["Files", result.files.length], ["Chunks indexed", result.chunks]].map(([k, v]) => (
                <div key={String(k)} className="bg-surface rounded-xl px-3 py-2">
                  <p className="text-muted text-xs">{k}</p>
                  <p className="text-slate-100 font-semibold">{v}</p>
                </div>
              ))}
            </div>
            <div className="flex flex-wrap gap-1.5">
              {result.files.map((name) => (
                <span key={name} className="text-[10px] font-mono bg-input text-muted px-2 py-0.5 rounded-full border border-border">📄 {name}</span>
              ))}
            </div>
            <p className="text-muted text-xs mt-4">Go to <strong className="text-slate-200">Chat</strong> and start asking questions.</p>
          </div>
        )}

        {/* Error */}
        {state === "error" && (
          <div className="bg-danger/10 border border-danger/30 rounded-xl px-4 py-3 flex items-start gap-2 text-danger text-sm animate-fade-in">
            <AlertCircle size={15} className="mt-0.5 shrink-0" />
            {err}
          </div>
        )}

        {/* Pipeline info cards */}
        <div className="grid grid-cols-3 gap-3 pt-2">
          {[
            ["FAISS", "Semantic vector search"],
            ["BM25", "Keyword retrieval"],
            ["CrossEncoder", "Neural reranking"],
          ].map(([title, desc]) => (
            <div key={title} className="bg-card border border-border rounded-xl p-4 text-center">
              <p className="text-accent font-mono text-xs font-semibold">{title}</p>
              <p className="text-dim text-[10px] mt-1">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
