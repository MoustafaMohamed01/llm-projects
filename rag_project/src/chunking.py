def split_into_chunks(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """
    Split text into chunks measured in *words* (not characters/tokens).

    Args:
        text: The full document text.
        chunk_size: Target number of words per chunk (default 400).
        overlap: Number of words shared between consecutive chunks (default 50).

    Returns:
        A list of text chunks (strings).

    How it works:
        1. Tokenise the text into words by splitting on whitespace.
        2. Slide a window of `chunk_size` words across the word list,
           stepping forward by `chunk_size - overlap` each time.
        3. Rejoin each window back into a string.
    """
    words = text.split()

    if not words:
        return []

    chunks = []
    step = chunk_size - overlap
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]        
        chunks.append(" ".join(chunk_words))    
        start += step                         

    return chunks
