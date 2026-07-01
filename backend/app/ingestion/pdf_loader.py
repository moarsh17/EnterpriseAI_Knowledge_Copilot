from pathlib import Path
from pypdf import PdfReader


class PDFLoader:
    """Extracts text from PDF files."""

    def load(self, pdf_path: Path) -> dict:

        reader = PdfReader(str(pdf_path))

        pages = []

        for index, page in enumerate(reader.pages, start=1):

            pages.append(
                {
                    "page": index,
                    "text": page.extract_text() or ""
                }
            )

        return {
            "filename": pdf_path.name,
            "total_pages": len(reader.pages),
            "pages": pages,
        }