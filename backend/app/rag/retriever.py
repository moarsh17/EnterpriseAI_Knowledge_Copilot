from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model
from app.rag.vectorstore import VECTOR_DB


class DocumentRetriever:

    def __init__(self):

        self.vectorstore = Chroma(
            persist_directory=str(VECTOR_DB),
            embedding_function=get_embedding_model(),
        )

    def get_retriever(
        self,
        k: int = 4,
        filters: dict | None = None,
    ):

        kwargs = {
            "k": k,
        }

        if filters:
            kwargs["filter"] = filters

        return self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs=kwargs,
        )

    def retrieve(
        self,
        query: str,
        k: int = 4,
        filters: dict | None = None,
    ):

        retriever = self.get_retriever(
            k=k,
            filters=filters,
        )

        return retriever.invoke(query)