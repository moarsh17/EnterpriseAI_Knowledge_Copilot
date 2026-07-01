from pathlib import Path
from app.ingestion.pdf_loader import PDFLoader

class IngestionService:

    def __init__(self):
        self.pdf_loader = PDFLoader()

    def ingest_pdf(self, pdf_path: Path):
        return self.pdf_loader.load(pdf_path)