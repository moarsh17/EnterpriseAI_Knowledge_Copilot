"""
Enterprise RAG Ingestion Pipeline.

Processes pages incrementally — each page is chunked, embedded, and stored
immediately, keeping memory consumption flat regardless of document size.

Returns a rich progress report including:
  - total_pages, processed_pages, failed_pages
  - ocr_pages, images_detected, tables_detected
  - chunks_created
  - processing_time_seconds
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Generator
from uuid import uuid4

from langchain_core.documents import Document as LangchainDocument

from app.core.logging import logger
from app.models.document import Document, Page
from app.rag.splitter import DocumentSplitter
from app.rag.vectorstore import get_vectorstore
from app.utils.metadata import MetadataExtractor


class RAGIngestionPipeline:

    def __init__(self):
        self.splitter = DocumentSplitter()
        self.vectorstore = get_vectorstore()

    # ------------------------------------------------------------------ #
    # Standard (batch) ingestion – used by DOCX, Excel, Image loaders    #
    # ------------------------------------------------------------------ #

    def ingest(self, document: Document) -> dict:
        """
        Batch ingestion for non-PDF loaders that produce a full Document.
        Splits all pages at once, embeds, stores, and returns a summary.
        """
        start = time.perf_counter()
        docs = self.splitter.split(document)
        self.vectorstore.add_documents(docs)
        elapsed = round(time.perf_counter() - start, 2)

        return {
            "document_id": document.document_id,
            "filename": document.filename,
            "total_pages": document.total_pages,
            "processed_pages": document.total_pages,
            "failed_pages": 0,
            "ocr_pages": 0,
            "images_detected": 0,
            "tables_detected": 0,
            "chunks_created": len(docs),
            "processing_time_seconds": elapsed,
        }

    # ------------------------------------------------------------------ #
    # Streaming incremental ingestion – used by PDFLoader                 #
    # ------------------------------------------------------------------ #

    def ingest_streaming(
        self,
        page_generator: Generator[Page, None, None],
        document_id: str,
        filename: str,
        document_type: str = "PDF",
        domain: str = "General",
        department: str = "General",
        extra_metadata: dict | None = None,
    ) -> dict:
        """
        Incrementally ingests pages from a generator.

        For each page yielded:
          1. Immediately split into chunks.
          2. Embed and store into ChromaDB.
          3. Accumulate progress counters.

        Memory footprint stays near-constant regardless of PDF size.
        """
        start = time.perf_counter()
        extra_metadata = extra_metadata or {}

        total_pages = 0
        failed_pages = 0
        ocr_pages = 0
        images_total = 0
        tables_total = 0
        chunks_total = 0

        # Sample text for metadata extraction (from the first page only)
        metadata_sample = ""

        for page in page_generator:
            total_pages += 1

            try:
                # Extract metadata from first meaningful page
                if not metadata_sample and page.text.strip():
                    metadata_sample = page.text[:1000]
                    meta = MetadataExtractor().extract(filename, metadata_sample)
                    domain = meta.get("domain", domain)
                    department = meta.get("department", department)

                # Build per-page metadata dict
                page_metadata = {
                    "document_id": document_id,
                    "filename": page.metadata.get("filename", filename),
                    "page": page.page_number,
                    "chunk_index": 0,            # overwritten in _split_page
                    "domain": domain,
                    "department": department,
                    "document_type": document_type,
                    "ocr_used": page.ocr_used,
                    "tables_detected": page.tables_detected,
                    "images_detected": page.images_detected,
                    "processing_timestamp": page.processing_timestamp.isoformat(),
                    **extra_metadata,
                    **page.metadata,
                }

                # Chunk and store immediately
                chunks = self._split_and_index_page(page, page_metadata)
                chunks_total += chunks

                # Update counters
                if page.ocr_used:
                    ocr_pages += 1
                images_total += page.images_detected
                tables_total += page.tables_detected

            except Exception as exc:
                failed_pages += 1
                logger.error(
                    f"[Pipeline] Failed to ingest page {page.page_number} "
                    f"of '{filename}': {exc}"
                )

        elapsed = round(time.perf_counter() - start, 2)

        return {
            "document_id": document_id,
            "filename": filename,
            "total_pages": total_pages,
            "processed_pages": total_pages - failed_pages,
            "failed_pages": failed_pages,
            "ocr_pages": ocr_pages,
            "images_detected": images_total,
            "tables_detected": tables_total,
            "chunks_created": chunks_total,
            "processing_time_seconds": elapsed,
        }

    # ------------------------------------------------------------------ #
    # Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _split_and_index_page(self, page: Page, base_metadata: dict) -> int:
        """
        Splits a single Page into chunks, assigns chunk_index, and stores
        them in ChromaDB. Returns the number of chunks created.
        """
        if not page.text.strip():
            return 0

        filename = base_metadata.get("filename", "")
        splitter = self.splitter._get_splitter_for_filename(filename)
        chunks = splitter.split_text(page.text)
        lc_docs: list[LangchainDocument] = []

        for i, chunk_text in enumerate(chunks):
            meta = {**base_metadata, "chunk_index": i}
            
            source_type = meta.get("source_type", "")
            if source_type == "github":
                file_path = meta.get("file_path", meta.get("filename", ""))
                repo_url = meta.get("repository_url", "")
                enriched_text = f"[Source File: {file_path}]\n[Repository: {repo_url}]\n\n{chunk_text}"
            else:
                enriched_text = chunk_text
                
            lc_docs.append(LangchainDocument(page_content=enriched_text, metadata=meta))

        if lc_docs:
            self.vectorstore.add_documents(lc_docs)

        return len(lc_docs)