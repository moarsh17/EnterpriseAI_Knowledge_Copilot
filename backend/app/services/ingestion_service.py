from pathlib import Path

from app.loaders.pdf_loader import PDFLoader
from app.rag.ingestion import RAGIngestionPipeline
from app.loaders.image_loader import ImageLoader
from app.loaders.docx_loader import DOCXLoader
from app.loaders.excel_loader import ExcelLoader    


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

    def ingest_docx(self, docx_path: Path):
        document = self.docx_loader.load(docx_path)
        chunks = self.pipeline.ingest(document)
        return {
            "document": document,
            "chunks_created": chunks,
        }


    def ingest_excel(self, excel_path: Path):
        document = self.excel_loader.load(excel_path)
        chunks = self.pipeline.ingest(document)
        return {
            "document": document,
            "chunks_created": chunks,
        }