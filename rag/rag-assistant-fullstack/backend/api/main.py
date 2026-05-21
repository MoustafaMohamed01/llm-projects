import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat   import router as chat_router
from api.upload import router as upload_router
from api.health import router as health_router

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

app = FastAPI(title="RAG Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)
