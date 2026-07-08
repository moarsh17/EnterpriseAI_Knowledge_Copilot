"""
Enterprise PDF Loader — streaming, memory-efficient, mixed-content capable.

Processing pipeline per page:
  1. Extract selectable text (pypdf / PyMuPDF native).
  2. If text is below OCR threshold → render page to image → run Tesseract.
  3. Extract embedded images → run Tesseract on each → append text.
  4. Extract tables → convert to structured key-value text → append.
  5. Wrap in fault-tolerant try/except; log and skip on page failure.

Each page is yielded immediately after processing to keep RAM flat.
"""

from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path
from typing import Generator
from uuid import uuid4

import fitz  # PyMuPDF
import numpy as np

from app.core.logging import logger
from app.models.document import Document, Page
from app.services.image_service import ImageService
from app.services.ocr_service import OCRService
from app.services.table_service import TableService
from app.utils.metadata import MetadataExtractor

# Minimum character count for a page's extracted text to be considered "meaningful".
# Pages below this threshold will be OCR-processed.
OCR_TEXT_THRESHOLD = 50

# Resolution multiplier when rendering a page to bitmap for OCR (2.0 ≈ 150 DPI)
PAGE_RENDER_SCALE = 2.0


class PDFLoader:
    """
    Enterprise streaming PDF loader.

    Usage:
        loader = PDFLoader()
        for page in loader.stream_pages(path, document_id, doc_meta):
            # page is a fully enriched Page model object
            ...
    """

    def __init__(self):
        self.ocr = OCRService()
        self.image_svc = ImageService()
        self.table_svc = TableService()

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def load(self, pdf_path: Path) -> Document:
        """
        Backward-compatible method: loads the entire PDF and returns a Document.

        For very large PDFs prefer stream_pages() + RAGIngestionPipeline directly.
        """
        document_id = str(uuid4())
        pages: list[Page] = []
        first_text_sample = ""

        for page in self.stream_pages(pdf_path, document_id):
            pages.append(page)
            if not first_text_sample:
                first_text_sample = page.text[:500]

        full_text = first_text_sample  # use sample for metadata extraction only
        metadata = MetadataExtractor().extract(pdf_path.name, full_text)

        return Document(
            document_id=document_id,
            filename=pdf_path.name,
            total_pages=len(pages),
            domain=metadata["domain"],
            department=metadata["department"],
            document_type="PDF",
            metadata=metadata,
            pages=pages,
        )

    def stream_pages(
        self,
        pdf_path: Path,
        document_id: str,
    ) -> Generator[Page, None, None]:
        """
        Generator that yields one enriched Page at a time.

        Memory usage is approximately constant with respect to PDF size because
        only one page's raw data exists in memory at a time.
        """
        pdf_path_str = str(pdf_path)

        with fitz.open(pdf_path_str) as pdf_doc:
            total_pages = len(pdf_doc)

            for page_index in range(total_pages):
                page_number = page_index + 1
                try:
                    yield self._process_page(
                        pdf_doc=pdf_doc,
                        page_index=page_index,
                        page_number=page_number,
                        pdf_path_str=pdf_path_str,
                    )
                except Exception as exc:
                    logger.error(
                        f"[PDF] Skipping page {page_number}/{total_pages} "
                        f"of '{pdf_path.name}' due to error: {exc}"
                    )

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    def _process_page(
        self,
        pdf_doc: fitz.Document,
        page_index: int,
        page_number: int,
        pdf_path_str: str,
    ) -> Page:
        fitz_page: fitz.Page = pdf_doc[page_index]

        # --- Step 1: Native text extraction ---
        raw_text = fitz_page.get_text("text") or ""
        ocr_used = False

        # --- Step 2: OCR if text is insufficient ---
        if len(raw_text.strip()) < OCR_TEXT_THRESHOLD:
            raw_text = self._ocr_page(fitz_page)
            ocr_used = True

        # --- Step 3: Embedded image OCR ---
        image_texts: list[str] = []
        for img_array in self.image_svc.extract_images_from_page(pdf_doc, fitz_page):
            img_text = self.ocr.extract_from_image_array(img_array)
            if img_text:
                image_texts.append(img_text)

        images_detected = len(image_texts)

        # --- Step 4: Table extraction ---
        table_text, tables_detected = self.table_svc.extract_from_page(
            pdf_path_str, page_number
        )

        # --- Step 5: Compose final page text ---
        parts = [raw_text]
        if image_texts:
            parts.append("\n".join(image_texts))
        if table_text:
            parts.append(table_text)

        full_page_text = "\n\n".join(p for p in parts if p.strip())

        return Page(
            page_number=page_number,
            text=full_page_text,
            ocr_used=ocr_used,
            tables_detected=tables_detected,
            images_detected=images_detected,
            processing_timestamp=datetime.utcnow(),
        )

    def _ocr_page(self, fitz_page: fitz.Page) -> str:
        """Render a page to a bitmap and run Tesseract on the result."""
        mat = fitz.Matrix(PAGE_RENDER_SCALE, PAGE_RENDER_SCALE)
        clip = fitz_page.rect
        pix: fitz.Pixmap = fitz_page.get_pixmap(matrix=mat, clip=clip, colorspace=fitz.csRGB)

        # Convert pixmap to numpy BGR array
        samples = pix.samples
        img_array = np.frombuffer(samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        bgr_array = img_array[:, :, ::-1].copy()  # RGB → BGR

        return self.ocr.extract_from_image_array(bgr_array)