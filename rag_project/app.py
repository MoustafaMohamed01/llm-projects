import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import streamlit as st
from loader import load_document
from chunking import split_into_chunks
from embeddings import embed_chunks
from vector_store import build_index, save_index, load_index
from retriever import retrieve
from generator import generate_answer

INDEX_DIR = os.path.join(os.path.dirname(__file__), "data", "index")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "uploads")
TOP_K = 3

st.set_page_config(
    page_title="RAG Chat",
    layout="wide",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0f0f0f;
    color: #e8e4d9;
  }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background-color: #1a1a1a;
    border-right: 1px solid #2a2a2a;
  }

  /* Chat input bar at bottom */
  [data-testid="stChatInput"] textarea {
    background-color: #1e1e1e;
    color: #e8e4d9;
    border: 1px solid #333;
    border-radius: 8px;
  }

  /* User message bubble */
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #1c1c2e;
    border-radius: 10px;
    padding: 0.5rem;
  }

  /* Assistant message bubble */
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #1a1a1a;
    border-radius: 10px;
    padding: 0.5rem;
  }

  /* Buttons */
  .stButton > button {
    background-color: #1e1e1e;
    color: #e8e4d9;
    border: 1px solid #333;
    border-radius: 8px;
    width: 100%;
  }
  .stButton > button:hover {
    border-color: #f0a500;
    color: #f0a500;
  }

  /* Headings */
  h1, h2, h3 { color: #e8e4d9; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("RAG Chat")
    st.caption("Upload a document to chat with it.")
    st.divider()

    st.subheader("Index a Document")

    uploaded_file = st.file_uploader(
        "Upload .txt or .pdf",
        type=["txt", "pdf"],
    )

    chunk_size = st.slider("Chunk size (words)", 200, 600, 400, step=50)
    overlap    = st.slider("Overlap (words)",     0,   100,  50, step=10)

    if st.button("Build Index"):
        if uploaded_file is None:
            st.warning("Please upload a document first.")
        else:
            with st.spinner("Processing…"):
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                text       = load_document(file_path)
                chunks     = split_into_chunks(text, chunk_size=chunk_size, overlap=overlap)
                embeddings = embed_chunks(chunks)
                index      = build_index(embeddings)
                save_index(index, chunks, INDEX_DIR)

            st.success(f"Indexed {len(chunks)} chunks!")

    st.divider()
    if os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        st.success("Index ready ✅")
    else:
        st.warning("No index yet.")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()     


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


question = st.chat_input("Ask a question about your document…")

if question:
    if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        st.error("No index found. Please upload and index a document in the sidebar first.")
        st.stop()

    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            index, chunks  = load_index(INDEX_DIR)
            top_chunks     = retrieve(question, index, chunks, top_k=TOP_K)
            answer         = generate_answer(question, top_chunks)

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
