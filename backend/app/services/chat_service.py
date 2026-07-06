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
                    filename=doc.metadata["filename"],
                    page=doc.metadata["page"],
                    chunk_index=doc.metadata["chunk_index"],
                )
            )

        logger.info("Answer generated successfully")

        return ChatResponse(
            question=question,
            answer=response["answer"],
            sources=sources,
        )