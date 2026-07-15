from pydantic import BaseModel
from typing import Optional


class Source(BaseModel):
    filename: str
    page: int
    chunk_index: int
    text: Optional[str] = None
    original_filename: Optional[str] = None
    source_type: Optional[str] = None
    repository_name: Optional[str] = None
    file_path: Optional[str] = None
    repository_url: Optional[str] = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]