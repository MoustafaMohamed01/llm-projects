# RAG Project Advanced

An advanced Retrieval-Augmented Generation (RAG) chatbot built with Python, Google Gemini, FAISS, hybrid retrieval, reranking, and Streamlit.

This project demonstrates a modular RAG pipeline that combines semantic search, keyword retrieval, reranking, and conversational memory to generate context-aware AI responses from custom documents.

---

# Features

* PDF and text document loading
* Smart document chunking
* Semantic search using FAISS
* BM25 keyword retrieval
* Hybrid retrieval system
* Cross-encoder reranking
* Conversational memory
* Gemini-powered answer generation
* Retrieval evaluation metrics
* Modern Streamlit chat interface

---

# Project Architecture

```bash id="fj4g6o"
rag_project_advanced/
│
├── data/
│
├── src/
│   ├── loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── reranker.py
│   ├── memory.py
│   ├── generator.py
│   ├── evaluation.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

# Technologies Used

* Python
* Google Gemini API
* Sentence Transformers
* FAISS
* BM25
* CrossEncoder Reranker
* Streamlit
* PyPDF

---

# How the System Works

## 1. Document Loading

The system loads PDF or text documents.

## 2. Chunking

Documents are split into smaller overlapping chunks for efficient retrieval.

## 3. Embedding Generation

Each chunk is converted into vector embeddings using Sentence Transformers.

## 4. Hybrid Retrieval

The system combines:

* Semantic similarity search (FAISS)
* Keyword-based retrieval (BM25)

## 5. Reranking

Retrieved chunks are reranked using a CrossEncoder model to improve relevance.

## 6. Prompt Generation

The most relevant chunks and recent chat history are sent to Gemini.

## 7. AI Response

Gemini generates a final context-aware answer.

---

# Conversation Memory

The chatbot remembers recent conversation history during the session using Streamlit session state.

This allows:

* follow-up questions
* contextual conversations
* better continuity

---

# Evaluation Metrics

The project includes a debug/evaluation system that can display:

* similarity scores
* BM25 scores
* reranking scores
* retrieval time
* generation time

---

# Installation

Clone the repository:

```bash id="ykh7qq"
https://github.com/MoustafaMohamed01/llm-projects.git
cd llm-projects/rag_project_advanced
```

Install dependencies:

```bash id="k6p6jf"
pip install --user -r requirements.txt
```

---

# Run the Application

```bash id="yyzckh"
streamlit run app.py
```

---

# Author

Moustafa Mohamed

GitHub: https://github.com/MoustafaMohamed01

LinkedIn: https://www.linkedin.com/in/moustafamohamed01/

Kaggle: https://www.kaggle.com/moustafamohamed01
