from langchain.retrievers import EnsembleRetriever
from langchain_chroma import Chroma

from app.rag.bm25 import BM25Search
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
        filters=None,
    ):

        kwargs = {
            "k": 4,
        }

        if filters:
            kwargs["filter"] = filters

        vector = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs=kwargs,
        )

        bm25 = BM25Search().get()

        return EnsembleRetriever(
            retrievers=[
                vector,
                bm25,
            ],
            weights=[
                0.7,
                0.3,
            ],
        )