from fastapi import APIRouter

from app.models.chat import ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)

service = ChatService()


@router.get("/", response_model=ChatResponse)
def chat(question: str):
    return service.ask(question)