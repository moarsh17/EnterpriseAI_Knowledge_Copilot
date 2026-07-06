from pathlib import Path

from app.core.constants import SUPPORTED_FILE_TYPES
from app.loaders.docx_loader import DOCXLoader
from app.loaders.excel_loader import ExcelLoader
from app.loaders.image_loader import ImageLoader
from app.loaders.pdf_loader import PDFLoader
from app.rag.ingestion import RAGIngestionPipeline


class IngestionService:

    def __init__(self):

        self.pipeline = RAGIngestionPipeline()

        self.loaders = {
            "pdf": PDFLoader(),
            "image": ImageLoader(),
            "docx": DOCXLoader(),
            "excel": ExcelLoader(),
        }

    def ingest(self, file_path: Path):

        extension = file_path.suffix.lower()

        if extension not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {extension}")

        loader_key = SUPPORTED_FILE_TYPES[extension]

        loader = self.loaders[loader_key]

        document = loader.load(file_path)

        chunks = self.pipeline.ingest(document)

        return {
            "document": document,
            "chunks_created": chunks,
        }