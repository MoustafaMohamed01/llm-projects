import os


def load_document(file_path: str) -> str:
    """
    Load and return the text content of a .txt or .pdf file.

    Args:
        file_path: Path to the document (relative or absolute).

    Returns:
        A single string containing all the text in the document.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return _load_txt(file_path)
    elif extension == ".pdf":
        return _load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type '{extension}'. Use .txt or .pdf.")


def _load_txt(file_path: str) -> str:
    """Read a plain-text file and return its contents."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _load_pdf(file_path: str) -> str:
    """
    Extract text from every page of a PDF using pypdf.
    Pages are joined with a newline so the text flows naturally.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required for PDF support. Run: pip install --user pypdf")

    reader = PdfReader(file_path)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:                    
            pages_text.append(text)

    return "\n".join(pages_text)
