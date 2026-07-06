from pathlib import Path
from uuid import uuid4

from docx import Document as DocxDocument

from app.models.document import Document, Page


class DOCXLoader:

    def load(self, docx_path: Path) -> Document:

        doc = DocxDocument(docx_path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        )

        return Document(
            document_id=str(uuid4()),
            filename=docx_path.name,
            total_pages=1,
            metadata={
                "type": "docx"
            },
            pages=[
                Page(
                    page_number=1,
                    text=text
                )
            ]
        )