from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document as LangchainDocument
from pathlib import Path

from app.models.document import Document


class DocumentSplitter:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.default_splitter = RecursiveCharacterTextSplitter(
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

    def _get_splitter_for_filename(self, filename: str):
        ext = Path(filename).suffix.lower()
        
        # Map common extensions to Langchain Language enum
        ext_map = {
            ".py": Language.PYTHON,
            ".js": Language.JS,
            ".ts": Language.TS,
            ".tsx": Language.TS,
            ".java": Language.JAVA,
            ".cpp": Language.CPP,
            ".c": Language.CPP,
            ".h": Language.CPP,
            ".go": Language.GO,
            ".md": Language.MARKDOWN,
            ".html": Language.HTML,
        }
        
        language = ext_map.get(ext)
        if language:
            return RecursiveCharacterTextSplitter.from_language(
                language=language, 
                chunk_size=self.chunk_size, 
                chunk_overlap=self.chunk_overlap
            )
        
        return self.default_splitter

    def split(self, document: Document):

        docs = []

        for page in document.pages:

            # Determine filename for this specific page (useful for multi-file documents like Github repos)
            page_filename = page.metadata.get("filename", document.filename)
            splitter = self._get_splitter_for_filename(page_filename)

            chunks = splitter.split_text(page.text)

            for index, chunk in enumerate(chunks):

                docs.append(
                    LangchainDocument(
                        page_content=chunk,
                        metadata={
                            "document_id": document.document_id,
                            "filename": page_filename,
                            "page": page.page_number,
                            "chunk_index": index,
                            "domain": document.domain,
                            "department": document.department,
                            "document_type": document.document_type,
                            **document.metadata,
                            **page.metadata,
                        },
                    )
                )

        return docs