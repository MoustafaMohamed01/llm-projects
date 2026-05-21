import io
import logging
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

import api.state as state
from src.chunking      import chunk_documents
from src.embeddings    import embed_texts
from src.vector_store  import build_index, save_index
from src.bm25_retriever import BM25Retriever

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE = 20 * 1024 * 1024  


def read_file_text(filename: str, raw: bytes) -> str:
    if filename.lower().endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")

    if filename.lower().endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"PDF read error: {e}")

    raise HTTPException(status_code=415, detail=f"Unsupported file type: {filename}")


@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    documents = []
    for uf in files:
        raw = await uf.read()

        if len(raw) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"'{uf.filename}' is over the 20 MB limit.")

        text = read_file_text(uf.filename, raw)
        if text.strip():
            documents.append({"source": uf.filename, "text": text})
            logger.info(f"Loaded '{uf.filename}' — {len(text)} chars")

    if not documents:
        raise HTTPException(status_code=422, detail="All files were empty or unreadable.")

    all_chunks = chunk_documents(documents)
    if not all_chunks:
        raise HTTPException(status_code=422, detail="Chunking produced no results.")

    texts      = [c["text"] for c in all_chunks]
    embeddings = embed_texts(texts)

    idx  = build_index(embeddings)
    save_index(idx, all_chunks)

    bm25 = BM25Retriever(all_chunks)

    state.faiss_index = idx
    state.chunks      = all_chunks
    state.bm25        = bm25

    logger.info(f"Indexed {len(all_chunks)} chunks from {len(documents)} file(s).")
    return {"success": True, "chunks": len(all_chunks), "files": [d["source"] for d in documents]}
