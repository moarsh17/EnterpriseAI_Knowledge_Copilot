from fastapi import FastAPI

from app.api.routes.upload import router as upload_router
from app.api.routes.chat import router as chat_router

app = FastAPI(
    title="ONGC Enterprise AI Knowledge Copilot",
    version="1.0.0",
)

app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "status": "running"
    }