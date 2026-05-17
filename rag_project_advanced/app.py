import time
import logging
import os

import streamlit as st

from src.loader import load_documents
from src.chunking import chunk_documents
from src.embeddings import embed_texts, embed_query
from src.vector_store import build_index, save_index, load_index, semantic_search
from src.bm25_retriever import BM25Retriever
from src.hybrid_retriever import hybrid_search
from src.reranker import rerank
from src.memory import add_message, get_recent_history, format_history_for_prompt, clear_history
from src.generator import configure_gemini, generate_answer
from src.evaluation import RetrievalStats, build_chunk_details, format_debug_markdown

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="RAG Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');
:root {
    --bg-primary:#0d0f14; --bg-secondary:#141720; --bg-card:#1a1d27;
    --bg-input:#1e2130; --border:#2a2f45; --accent:#4f8ef7;
    --accent-glow:rgba(79,142,247,0.15); --text-primary:#e8eaf2;
    --text-secondary:#8b90a8; --text-muted:#5a5f78;
    --success:#4eca8b; --warning:#f0a040;
    --mono:'IBM Plex Mono',monospace; --sans:'Inter',sans-serif;
}
html,body,[class*="css"]{font-family:var(--sans);background-color:var(--bg-primary);color:var(--text-primary);}
section[data-testid="stSidebar"]{background-color:var(--bg-secondary)!important;border-right:1px solid var(--border);}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{color:var(--text-primary);}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label{color:var(--text-secondary);font-size:0.85rem;}
.main .block-container{padding-top:1.5rem;padding-bottom:6rem;max-width:860px;margin:0 auto;}
.rag-header{display:flex;align-items:center;gap:0.75rem;padding:1rem 0 1.5rem 0;border-bottom:1px solid var(--border);margin-bottom:1.5rem;}
.rag-header h1{font-family:var(--mono);font-size:1.4rem;font-weight:600;color:var(--accent);margin:0;}
.rag-header span{color:var(--text-muted);font-size:0.8rem;font-family:var(--mono);}
[data-testid="stChatMessage"]{background-color:transparent!important;border:none!important;padding:0.25rem 0;}
[data-testid="stChatInput"]{background:var(--bg-input)!important;border:1px solid var(--border)!important;border-radius:12px!important;}
[data-testid="stChatInput"]:focus-within{border-color:var(--accent)!important;box-shadow:0 0 0 3px var(--accent-glow)!important;}
[data-testid="stChatInput"] textarea{color:var(--text-primary)!important;background:transparent!important;}
.status-pill{display:inline-flex;align-items:center;gap:0.4rem;background:var(--bg-card);border:1px solid var(--border);border-radius:20px;padding:0.25rem 0.75rem;font-family:var(--mono);font-size:0.73rem;color:var(--text-secondary);margin:0.2rem;}
.status-pill.green{border-color:var(--success);color:var(--success);}
.status-pill.blue{border-color:var(--accent);color:var(--accent);}
.status-pill.warn{border-color:var(--warning);color:var(--warning);}
.stButton>button{background:var(--bg-card)!important;color:var(--text-secondary)!important;border:1px solid var(--border)!important;border-radius:8px!important;font-family:var(--mono)!important;font-size:0.78rem!important;transition:all 0.15s ease;}
.stButton>button:hover{border-color:var(--accent)!important;color:var(--accent)!important;background:var(--accent-glow)!important;}
table{border-collapse:collapse;width:100%;font-size:0.78rem;font-family:var(--mono);}
th{background:var(--bg-card);color:var(--accent);padding:6px 10px;border:1px solid var(--border);text-align:left;}
td{padding:5px 10px;border:1px solid var(--border);color:var(--text-secondary);word-break:break-word;}
tr:nth-child(even) td{background:var(--bg-secondary);}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:var(--bg-primary);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
""", unsafe_allow_html=True)


defaults = {
    "messages":     [],
    "memory":       [],
    "faiss_index":  None,
    "chunks":       None,
    "bm25":         None,
    "system_ready": False,
    "last_stats":   None,
    "gemini_ok":    False,
    "build_error":  None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v



def save_uploaded_files(uploaded_files) -> tuple[list[dict], str | None]:
    """
    Save Streamlit UploadedFile objects to data/ and read their text.
    Returns (documents_list, error_or_None).
    """
    import io
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    documents = []
    for uf in uploaded_files:
        file_path = os.path.join(data_dir, uf.name)
        raw_bytes = uf.read()

        with open(file_path, "wb") as f:
            f.write(raw_bytes)

        ext = os.path.splitext(uf.name)[1].lower()
        try:
            if ext == ".pdf":
                import PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
                text = "\n".join(
                    p.extract_text() or "" for p in reader.pages
                )
            elif ext == ".txt":
                text = raw_bytes.decode("utf-8", errors="ignore")
            else:
                continue

            if text.strip():
                documents.append({"source": uf.name, "text": text})
        except Exception as e:
            return [], f"Failed to read '{uf.name}': {e}"

    if not documents:
        return [], "Uploaded files contained no readable text."

    return documents, None


def do_build_index(documents: list[dict]):
    """
    Chunk → embed → FAISS + BM25 from a pre-loaded documents list.
    Writes results into st.session_state and returns error string or None.
    """
    progress = st.progress(0, text=f" Chunking {len(documents)} document(s)…")

    chunks = chunk_documents(documents)
    if not chunks:
        return "Documents were loaded but chunking produced no text."

    progress.progress(30, text=f"Generating embeddings for {len(chunks)} chunks…")

    chunk_texts = [c["text"] for c in chunks]
    embeddings  = embed_texts(chunk_texts)

    progress.progress(70, text=" Building FAISS index…")

    faiss_index = build_index(embeddings)
    save_index(faiss_index, chunks)

    progress.progress(90, text="Building BM25 index…")

    bm25 = BM25Retriever(chunks)

    st.session_state["faiss_index"]  = faiss_index
    st.session_state["chunks"]       = chunks
    st.session_state["bm25"]         = bm25
    st.session_state["system_ready"] = True
    st.session_state["build_error"]  = None

    progress.progress(100, text=f"Indexed {len(chunks)} chunks from {len(documents)} file(s).")
    time.sleep(0.8)
    progress.empty()
    return None



with st.sidebar:
    st.markdown("## Settings")
    st.markdown("### Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload one or more PDF or TXT files, then click Build Index.",
    )

    if uploaded_files:
        st.caption(f"📎 {len(uploaded_files)} file(s) ready — click Build Index below.")

    build_clicked = st.button(
        "Build Index",
        use_container_width=True,
        disabled=(not uploaded_files), 
        help="Upload files first, then click here to index them.",
    )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state["messages"]   = []
        st.session_state["memory"]     = clear_history()
        st.session_state["last_stats"] = None
        st.rerun()

    st.divider()
    st.markdown("### Debug")
    show_debug = st.toggle("Show retrieval debug panel", value=False)

    st.divider()
    st.markdown("<span style='font-size:0.72rem;color:#5a5f78;'>Advanced RAG · Hybrid Search · CrossEncoder · Gemini 2.5 Flash</span>",
                unsafe_allow_html=True)


if build_clicked and uploaded_files:
    st.session_state["system_ready"] = False
    st.session_state["build_error"]  = None

    with st.spinner("Reading uploaded files…"):
        documents, read_error = save_uploaded_files(uploaded_files)

    if read_error:
        st.session_state["build_error"] = read_error
    else:
        error = do_build_index(documents)
        if error:
            st.session_state["build_error"]  = error
            st.session_state["system_ready"] = False

    st.rerun()

if not st.session_state["gemini_ok"]:
    try:
        configure_gemini()
        st.session_state["gemini_ok"] = True
    except Exception as e:
        st.error(f"Gemini config error: {e}")



st.markdown("""
<div class="rag-header">
  <div>
    <h1>RAG Assistant</h1>
    <span>Hybrid Search · Reranking · Gemini 2.5 Flash</span>
  </div>
</div>
""", unsafe_allow_html=True)

if st.session_state["build_error"]:
    st.warning(f"{st.session_state['build_error']}")
    st.info("Put PDF or TXT files inside the `data/` folder, then click **Build Index**.")

if st.session_state["system_ready"]:
    n = len(st.session_state["chunks"])
    st.markdown(
        f'<span class="status-pill green">✓ {n} chunks indexed</span>'
        f'<span class="status-pill blue">Hybrid Search</span>'
        f'<span class="status-pill blue">CrossEncoder</span>'
        f'<span class="status-pill green">Gemini Ready</span>',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<span class="status-pill warn">⚠ No documents indexed — add files to data/ and click Build Index</span>',
                unsafe_allow_html=True)



for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if show_debug and st.session_state.get("last_stats"):
    with st.expander("🔬 Last Query · Retrieval Debug", expanded=False):
        st.markdown(format_debug_markdown(st.session_state["last_stats"]))



def run_rag_pipeline(query: str) -> tuple[str, RetrievalStats]:
    stats = RetrievalStats(query=query)

    q_emb = embed_query(query)

    t0 = time.time()
    hybrid_results = hybrid_search(
        query=query,
        query_embedding=q_emb,
        faiss_index=st.session_state["faiss_index"],
        chunks=st.session_state["chunks"],
        bm25_retriever=st.session_state["bm25"],
        top_k=15,
        semantic_weight=1.0,
        bm25_weight=1.0,
    )
    sem_res  = semantic_search(q_emb, st.session_state["faiss_index"], st.session_state["chunks"], top_k=15)
    bm25_res = st.session_state["bm25"].search(query, top_k=15)
    stats.semantic_count = len(sem_res)
    stats.bm25_count     = len(bm25_res)
    stats.hybrid_count   = len(hybrid_results)
    stats.retrieval_time = time.time() - t0

    t1 = time.time()
    reranked = rerank(query=query, candidates=hybrid_results, top_k=5)
    stats.reranking_time = time.time() - t1
    stats.final_count    = len(reranked)
    stats.chunk_details  = build_chunk_details(reranked)

    recent       = get_recent_history(st.session_state["memory"], max_exchanges=4)
    history_text = format_history_for_prompt(recent)

    answer, gen_time = generate_answer(
        context_chunks=reranked,
        conversation_history_text=history_text,
        question=query,
    )
    stats.generation_time = gen_time
    return answer, stats



if prompt := st.chat_input("Ask a question about your documents…"):

    if not st.session_state["system_ready"]:
        st.warning("Index not ready. Add files to data/ and click ** Build Index**.")
        st.stop()

    if not st.session_state["gemini_ok"]:
        st.error("Gemini API not configured. Check the API key in src/generator.py.")
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.session_state["memory"] = add_message(st.session_state["memory"], "user", prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            answer, stats = run_rag_pipeline(prompt)
        st.markdown(answer)

    st.session_state["memory"] = add_message(st.session_state["memory"], "assistant", answer)
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.session_state["last_stats"] = stats

    if show_debug:
        with st.expander(f"Debug · {stats.final_count} chunks · {stats.total_time:.2f}s", expanded=True):
            st.markdown(format_debug_markdown(stats))

    st.rerun()
