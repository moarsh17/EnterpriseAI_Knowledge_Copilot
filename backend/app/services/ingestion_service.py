from pathlib import Path

from app.loaders.pdf_loader import PDFLoader
from app.rag.ingestion import RAGIngestionPipeline


class IngestionService:

    def __init__(self):
        self.loader = PDFLoader()
        self.pipeline = RAGIngestionPipeline()

    def ingest_pdf(self, pdf_path: Path):
        document = self.loader.load(pdf_path)
        chunks = self.pipeline.ingest(document)
        return {
            "document": document,
            "chunks_created": chunks,
        }