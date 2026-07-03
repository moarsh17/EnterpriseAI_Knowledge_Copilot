from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model
from app.rag.vectorstore import VECTOR_DB


class DocumentRetriever:

    def __init__(self):

        self.vectorstore = Chroma(
            persist_directory=str(VECTOR_DB),
            embedding_function=get_embedding_model(),
        )

    def get_retriever(self, k: int = 4):

        return self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 4,
                "fetch_k": 10,
            },
        )

    def retrieve(self, query: str, k: int = 4):

        retriever = self.get_retriever(k)

        return retriever.invoke(query)