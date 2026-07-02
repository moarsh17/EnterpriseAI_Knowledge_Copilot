from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class Page(BaseModel):
    page_number: int
    text: str


class Document(BaseModel):
    document_id: str
    filename: str
    total_pages: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)
    pages: List[Page]