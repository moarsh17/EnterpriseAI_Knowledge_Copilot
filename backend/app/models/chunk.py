from typing import Optional
from pydantic import BaseModel

class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    page_number: int
    chunk_index: int
    text: str
    metadata: Optional[dict] = {}