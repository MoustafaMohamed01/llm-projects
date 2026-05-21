# Fullstack Rag Assistant

A modern fullstack Retrieval-Augmented Generation (RAG) AI assistant built with FastAPI, Next.js, FAISS, BM25, CrossEncoder reranking, and Google Gemini.

The system allows users to upload documents and chat with them through a modern AI chat interface powered by a hybrid retrieval pipeline.

---

# Features

## AI & RAG Features

- Semantic search using FAISS
- BM25 keyword retrieval
- Hybrid retrieval pipeline
- Reciprocal Rank Fusion (RRF)
- CrossEncoder reranking
- Conversational memory
- Gemini-powered answer generation
- Context-aware responses
- Debug retrieval metrics

---

## Fullstack Features

- FastAPI backend
- Next.js frontend
- Modern AI chat UI
- Dark mode interface
- Drag & drop file upload
- Markdown rendering
- Code block rendering
- Responsive design
- Sidebar navigation
- Upload progress feedback

---

# Tech Stack

## Frontend

- Next.js
- React
- Tailwind CSS
- TypeScript

## Backend

- FastAPI
- Python

## AI / ML

- Google Gemini
- Sentence Transformers
- FAISS
- BM25
- CrossEncoder Reranker

---

# Project Architecture

```bash id="arch1"
ragflow-ai/
│
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   ├── chat.py
│   │   ├── upload.py
│   │   └── health.py
│   │
│   ├── src/
│   │   ├── config.py
│   │   ├── loader.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── bm25_retriever.py
│   │   ├── hybrid_retriever.py
│   │   ├── reranker.py
│   │   ├── memory.py
│   │   ├── generator.py
│   │   └── evaluation.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
└── README.md
```

---

# How the System Works

## 1. Document Upload

Users upload:

- PDF files
- TXT files

The backend:

- extracts text
- splits text into chunks
- creates embeddings
- builds FAISS index
- builds BM25 corpus

---

## 2. Hybrid Retrieval

The system performs:

- semantic retrieval using FAISS
- keyword retrieval using BM25

Results are merged using:

- Reciprocal Rank Fusion (RRF)

---

## 3. Reranking

Retrieved chunks are reranked using a CrossEncoder model to improve relevance quality.

---

## 4. Gemini Generation

The best chunks plus conversation history are sent to Gemini to generate a grounded response.

---

# RAG Pipeline

```text id="pipeline2"
User Question
     ↓
Embedding Generation
     ↓
FAISS Retrieval
     +
BM25 Retrieval
     ↓
RRF Fusion
     ↓
CrossEncoder Reranking
     ↓
Best Context Chunks
     ↓
Gemini 2.5 Flash
     ↓
Final AI Response
```

---

# Installation

## Backend

```bash id="installbackend"
cd backend
pip install -r requirements.txt
```

---

## Add Gemini API Key

Open:

```text id="configpath"
backend/src/config.py
```

Add your API key:

```python id="apikey"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

---

## Start Backend

```bash id="runbackend"
uvicorn api.main:app --reload --port 8000
```

---

# Frontend

```bash id="installfrontend"
cd frontend
npm install
npm run dev
```

---

# Open Application

```text id="openapp"
http://localhost:3000
```

---

# Pages

| Page      | Description                       |
| --------- | --------------------------------- |
| `/chat`   | AI document chat interface        |
| `/upload` | Upload PDF/TXT files              |
| `/about`  | Project overview and architecture |

---

# Debug Features

Optional debug panel includes:

- retrieved chunks
- semantic similarity scores
- BM25 scores
- reranking scores
- latency metrics

---

# Example Questions

- "What skills are mentioned in the documents?"
- "Summarize the experience section."
- "Explain the deep learning projects."
- "What AI technologies are used?"

---

# Design Goals

This project was built to:

- learn modern RAG systems
- understand hybrid retrieval
- practice AI engineering
- build fullstack AI applications
- create portfolio-ready AI projects

---

# Future Improvements

- Multi-user support
- Authentication
- Persistent vector database
- Streaming responses
- Local LLM support
- Docker deployment
- Cloud deployment
- Multi-document collections

---

# Author

Moustafa Mohamed

GitHub:
https://github.com/MoustafaMohamed01

LinkedIn:
https://www.linkedin.com/in/moustafamohamed01/

Kaggle:
https://www.kaggle.com/moustafamohamed01
