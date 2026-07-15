from app.models import response
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama

from app.rag.prompts import RAG_PROMPT, CONTEXTUALIZE_Q_PROMPT
from app.rag.retriever import DocumentRetriever
from app.rag.memory import memory


class RAGChain:

    def __init__(self):

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0,
        )

        self.prompt = RAG_PROMPT

    def invoke(
        self,
        question: str,
        filters: dict | None = None,
    ):

        retriever = DocumentRetriever().get_retriever(
            filters=filters,
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, CONTEXTUALIZE_Q_PROMPT
        )

        document_chain = create_stuff_documents_chain(
            self.llm,
            self.prompt,
        )

        chain = create_retrieval_chain(
            history_aware_retriever,
            document_chain,
        )

        response = chain.invoke(
            {
                "input": question,
                "chat_history": memory.load_memory_variables({})["chat_history"],
            }
        )

        memory.save_context(
            {"input": question},
            {"output": response["answer"]},
        )

        return response