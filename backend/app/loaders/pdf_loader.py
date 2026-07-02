from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from app.models.document import Document, Page


class PDFLoader:

    def load(self, pdf_path: Path) -> Document:

        reader = PdfReader(str(pdf_path))

        pages = []

        for index, page in enumerate(reader.pages, start=1):

            pages.append(
                Page(
                    page_number=index,
                    text=page.extract_text() or ""
                )
            )

        return Document(
            document_id=str(uuid4()),
            filename=pdf_path.name,
            total_pages=len(reader.pages),
            pages=pages
        )