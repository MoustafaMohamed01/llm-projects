# Simple RAG Chatbot (Gemini + FAISS)

A beginner-friendly **Retrieval-Augmented Generation (RAG)** project that allows users to ask questions about custom documents and get AI-generated answers using Google Gemini and vector search.

---

## Features

* Load and process text/PDF documents
* Split documents into chunks for better retrieval
* Generate embeddings using Sentence Transformers
* Store and search embeddings using FAISS
* Retrieve relevant context based on user queries
* Generate answers using Gemini API
* Simple Streamlit chat interface

---

## Tech Stack

* Python
* Google Gemini API
* FAISS (Vector Database)
* Sentence-Transformers (Embeddings)
* Streamlit (UI)
* PyPDF (Document loading)

---

## Project Structure

```
rag_project/
│
├── data/                 # Documents
├── src/
│   ├── loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── generator.py
│
├── app.py               # Streamlit app
├── requirements.txt
└── README.md
```

---

## Installation

Install dependencies:

```bash
pip install --user -r requirements.txt
```

---


## Run the Project

```bash
streamlit run app.py
```

---

## How It Works

1. Document is loaded and split into chunks
2. Each chunk is converted into embeddings
3. FAISS stores embeddings for fast similarity search
4. User asks a question
5. Relevant chunks are retrieved
6. Gemini generates an answer using retrieved context
