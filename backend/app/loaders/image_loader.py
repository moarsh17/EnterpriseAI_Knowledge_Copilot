from pathlib import Path
from uuid import uuid4

from app.models.document import Document, Page
from app.services.ocr_service import OCRService


class ImageLoader:

    def __init__(self):

        self.ocr = OCRService()

    def load(self, image_path: Path) -> Document:

        text = self.ocr.extract_text(image_path)

        return Document(
            document_id=str(uuid4()),
            filename=image_path.name,
            total_pages=1,
            metadata={
                "type": "image"
            },
            pages=[
                Page(
                    page_number=1,
                    text=text,
                )
            ],
        )