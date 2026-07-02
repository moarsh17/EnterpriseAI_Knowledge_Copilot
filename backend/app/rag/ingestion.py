from app.models.document import Document
from app.rag.splitter import DocumentSplitter
from app.rag.vectorstore import get_vectorstore


class RAGIngestionPipeline:

    def __init__(self):
        self.splitter = DocumentSplitter()
        self.vectorstore = get_vectorstore()

    def ingest(self, document: Document):
        docs = self.splitter.split(document)
        self.vectorstore.add_documents(docs)
        return len(docs)