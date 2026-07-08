from langchain_community.retrievers import BM25Retriever

from app.rag.vectorstore import get_vectorstore


class BM25Search:

    def __init__(self):

        vectorstore = get_vectorstore()

        docs = vectorstore.get()

        texts = docs.get("documents", [])

        if not texts:
            self.retriever = None
            return

        metadatas = docs.get("metadatas", [])

        from langchain_core.documents import Document

        documents = [
            Document(
                page_content=text,
                metadata=metadata,
            )
            for text, metadata in zip(texts, metadatas)
        ]

        self.retriever = BM25Retriever.from_documents(documents)

        self.retriever.k = 4

    def get(self):

        return self.retriever