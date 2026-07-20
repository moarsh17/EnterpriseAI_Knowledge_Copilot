from fastapi import APIRouter

from app.models.chat import ChatResponse
from app.services.chat_service import ChatService
from app.rag.memory import clear_memory

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)

service = ChatService()


@router.delete("/memory")
def clear_chat_memory():
    clear_memory()
    return {"status": "success", "message": "Chat memory cleared successfully."}


@router.get("/", response_model=ChatResponse)
def chat(
    question: str,
    domain: str | None = None,
    department: str | None = None,
    document_type: str | None = None,
):

    return service.ask(
        question=question,
        domain=domain,
        department=department,
        document_type=document_type,
    )