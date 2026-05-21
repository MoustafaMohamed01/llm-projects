const API = "http://localhost:8000";

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface DebugChunk {
  rank: number;
  source: string;
  text_preview: string;
  semantic_score: number;
  bm25_score: number;
  reranker_score: number;
}

export interface ChatResult {
  answer: string;
  sources: string[];
  debug: {
    chunks: DebugChunk[];
    retrieval_time: number;
    reranking_time: number;
    generation_time: number;
    total_time: number;
  };
}

export interface UploadResult {
  success: boolean;
  chunks: number;
  files: string[];
}

export async function chat(message: string, history: Message[]): Promise<ChatResult> {
  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Error ${res.status}`);
  }
  return res.json();
}

export async function upload(files: File[]): Promise<UploadResult> {
  const form = new FormData();
  files.forEach((f) => form.append("files", f));
  const res = await fetch(`${API}/upload`, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Error ${res.status}`);
  }
  return res.json();
}

export async function health() {
  const res = await fetch(`${API}/health`);
  return res.json();
}
