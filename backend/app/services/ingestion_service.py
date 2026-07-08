"""
Ingestion Service — routes uploaded files to the correct loader and pipeline.

PDFs are routed through the streaming incremental pipeline (PDFLoader.stream_pages).
All other formats (DOCX, Excel, Image) use the existing batch pipeline.
"""

from pathlib import Path
from uuid import uuid4

from app.core.constants import SUPPORTED_FILE_TYPES
from app.loaders.docx_loader import DOCXLoader
from app.loaders.excel_loader import ExcelLoader
from app.loaders.image_loader import ImageLoader
from app.loaders.pdf_loader import PDFLoader
from app.rag.ingestion import RAGIngestionPipeline


class IngestionService:

    def __init__(self):
        self.pipeline = RAGIngestionPipeline()
        self.pdf_loader = PDFLoader()

        self.batch_loaders = {
            "image": ImageLoader(),
            "docx": DOCXLoader(),
            "excel": ExcelLoader(),
        }

    def ingest(self, file_path: Path) -> dict:
        extension = file_path.suffix.lower()

        if extension not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {extension}")

        loader_key = SUPPORTED_FILE_TYPES[extension]

        # --- PDF: stream pages incrementally ---
        if loader_key == "pdf":
            document_id = str(uuid4())
            page_gen = self.pdf_loader.stream_pages(file_path, document_id)
            report = self.pipeline.ingest_streaming(
                page_generator=page_gen,
                document_id=document_id,
                filename=file_path.name,
                document_type="PDF",
            )
            return report

        # --- All other types: batch load then ingest ---
        loader = self.batch_loaders[loader_key]
        document = loader.load(file_path)
        report = self.pipeline.ingest(document)
        return report