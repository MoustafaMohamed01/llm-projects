faiss_index = None  
chunks      = []     
bm25        = None   


def is_ready():
    return faiss_index is not None and len(chunks) > 0 and bm25 is not None
