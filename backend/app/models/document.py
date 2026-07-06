from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Page(BaseModel):
    page_number: int
    text: str


class Document(BaseModel):
    document_id: str

    filename: str

    total_pages: int

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    domain: str = "General"

    department: str = "General"

    document_type: str = "Unknown"

    tags: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    pages: list[Page]