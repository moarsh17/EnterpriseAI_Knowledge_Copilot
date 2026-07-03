from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama

from app.rag.prompts import RAG_PROMPT
from app.rag.retriever import DocumentRetriever


class RAGChain:

    def __init__(self):

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0,
        )

        self.retriever = DocumentRetriever().get_retriever()

        self.document_chain = create_stuff_documents_chain(
            self.llm,
            RAG_PROMPT,
        )

        self.chain = create_retrieval_chain(
            self.retriever,
            self.document_chain,
        )

    def invoke(self, question: str):

        return self.chain.invoke(
            {
                "input": question
            }
        )