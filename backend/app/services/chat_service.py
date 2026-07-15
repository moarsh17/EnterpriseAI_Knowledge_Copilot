from app.core.logging import logger
from app.core.rag_engine import RAGEngine
from app.models.chat import ChatResponse, Source


class ChatService:

    def __init__(self):

        self.chain = RAGEngine.get_instance()

    def ask(
        self,
        question: str,
        domain: str | None = None,
        department: str | None = None,
        document_type: str | None = None,
    ):

        logger.info(f"Question: {question}")

        filters = {}

        if domain:
            filters["domain"] = domain

        if department:
            filters["department"] = department

        if document_type:
            filters["document_type"] = document_type

        response = self.chain.invoke(
            question,
            filters if filters else None,
        )

        sources = []

        for doc in response["context"]:

            sources.append(
                Source(
                    filename=doc.metadata.get("filename", ""),
                    page=doc.metadata.get("page", 1),
                    chunk_index=doc.metadata.get("chunk_index", 0),
                    text=doc.page_content,
                    original_filename=doc.metadata.get("original_filename"),
                    source_type=doc.metadata.get("source_type"),
                    repository_name=doc.metadata.get("repository_name"),
                    file_path=doc.metadata.get("file_path"),
                    repository_url=doc.metadata.get("repository_url")
                )
            )

        logger.info("Answer generated successfully")

        return ChatResponse(
            question=question,
            answer=response["answer"],
            sources=sources,
        )