from app.core.logging import logger
from app.models.chat import ChatResponse, Source
from app.rag.chain import RAGChain


class ChatService:

    def __init__(self):
        self.chain = RAGChain()

    def ask(self, question: str):

        logger.info(f"Question: {question}")

        response = self.chain.invoke(question)

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