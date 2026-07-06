from app.rag.chain import RAGChain


class RAGEngine:

    _instance = None

    @classmethod
    def get_instance(cls):

        if cls._instance is None:
            cls._instance = RAGChain()

        return cls._instance