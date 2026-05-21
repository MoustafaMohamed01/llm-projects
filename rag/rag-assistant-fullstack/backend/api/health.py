from fastapi import APIRouter
import api.state as state

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "index_ready": state.is_ready(),
        "chunks_loaded": len(state.chunks),
    }
