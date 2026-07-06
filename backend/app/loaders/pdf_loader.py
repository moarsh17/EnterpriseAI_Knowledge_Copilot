from pathlib import Path
from uuid import uuid4

from pypdf import PdfReader

from app.models.document import Document, Page
from app.utils.metadata import MetadataExtractor


class PDFLoader:

    def load(self, pdf_path: Path) -> Document:

        reader = PdfReader(pdf_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            pages.append(
                Page(
                    page_number=page_number,
                    text=page.extract_text() or "",
                )
            )

        full_text = "\n".join(page.text for page in pages)

        metadata = MetadataExtractor().extract(
            pdf_path.name,
            full_text,
        )

        return Document(
            document_id=str(uuid4()),
            filename=pdf_path.name,
            total_pages=len(pages),
            domain=metadata["domain"],
            department=metadata["department"],
            document_type="PDF",
            metadata=metadata,
            pages=pages,
        )