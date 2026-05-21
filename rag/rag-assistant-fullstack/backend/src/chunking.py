import re
import logging

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def split_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[str]:
    
    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())

        step = chunk_size - chunk_overlap
        start += step

    return chunks


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:
   
    all_chunks = []
    chunk_id = 0

    for doc in documents:
        doc_chunks = split_into_chunks(
            doc["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        logger.info(f"'{doc['source']}' → {len(doc_chunks)} chunks")

        for chunk_text in doc_chunks:
            all_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "source": doc["source"],
                    "text": chunk_text,
                }
            )
            chunk_id += 1

    logger.info(f"Total chunks created: {len(all_chunks)}")
    return all_chunks
