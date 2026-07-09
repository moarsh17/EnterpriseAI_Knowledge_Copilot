from fastapi import FastAPI

from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router
from app.api.routes.documents import router as documents_router
from app.api.routes.github import router as github_router
from app.core.rag_engine import RAGEngine

RAGEngine.get_instance()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ONGC Enterprise AI Knowledge Copilot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(github_router)


@app.get("/")
def root():
    return {
        "status": "running"
    }