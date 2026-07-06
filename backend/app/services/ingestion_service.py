from pathlib import Path

from app.loaders.pdf_loader import PDFLoader
from app.rag.ingestion import RAGIngestionPipeline
from app.loaders.image_loader import ImageLoader


class IngestionService:

    def __init__(self):
        self.loader = PDFLoader()
        self.pipeline = RAGIngestionPipeline()
        self.image_loader = ImageLoader()

    def ingest_pdf(self, pdf_path: Path):
        document = self.loader.load(pdf_path)
        chunks = self.pipeline.ingest(document)
        return {
            "document": document,
            "chunks_created": chunks,
        }

    def ingest_image(self, image_path: Path):
        document = self.image_loader.load(image_path)
        chunks = self.pipeline.ingest(document)
        return {
            "document": document,
            "chunks_created": chunks,
        }