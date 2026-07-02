from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangchainDocument

from app.models.document import Document


class DocumentSplitter:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(self, document: Document):

        docs = []

        for page in document.pages:

            chunks = self.splitter.split_text(page.text)

            for index, chunk in enumerate(chunks):

                docs.append(
                    LangchainDocument(
                        page_content=chunk,
                        metadata={
                            "document_id": document.document_id,
                            "filename": document.filename,
                            "page": page.page_number,
                            "chunk_index": index,
                            **document.metadata,
                        },
                    )
                )

        return docs