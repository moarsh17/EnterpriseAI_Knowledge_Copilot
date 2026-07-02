from langchain_chroma import Chroma

from app.core.config import BASE_DIR
from app.rag.embeddings import get_embedding_model


VECTOR_DB = BASE_DIR / "data" / "chroma"


def get_vectorstore():

    return Chroma(
        persist_directory=str(VECTOR_DB),
        embedding_function=get_embedding_model(),
    )