from pydantic import BaseModel


class Source(BaseModel):
    filename: str
    page: int
    chunk_index: int


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]