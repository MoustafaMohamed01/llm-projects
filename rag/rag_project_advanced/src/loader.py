import os
import logging

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

logger = logging.getLogger(__name__)


def load_pdf(file_path: str) -> str:
    
    if PyPDF2 is None:
        raise ImportError("PyPDF2 is not installed. Run: pip install PyPDF2")

    text = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
            else:
                logger.warning(f"Page {page_num + 1} in '{file_path}' returned no text.")

    return "\n".join(text)


def load_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_documents(data_dir: str = "data") -> list[dict]:
    
    documents = []

    if not os.path.exists(data_dir):
        logger.warning(f"Data directory '{data_dir}' does not exist.")
        return documents

    supported_extensions = {".pdf", ".txt"}

    for filename in sorted(os.listdir(data_dir)):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_extensions:
            continue

        file_path = os.path.join(data_dir, filename)
        logger.info(f"Loading: {filename}")

        try:
            if ext == ".pdf":
                text = load_pdf(file_path)
            elif ext == ".txt":
                text = load_text(file_path)
            else:
                continue

            if text.strip():
                documents.append({"source": filename, "text": text})
                logger.info(f"  → Loaded {len(text)} characters from '{filename}'")
            else:
                logger.warning(f"  → '{filename}' appears to be empty after extraction.")

        except Exception as e:
            logger.error(f"  → Failed to load '{filename}': {e}")

    return documents
