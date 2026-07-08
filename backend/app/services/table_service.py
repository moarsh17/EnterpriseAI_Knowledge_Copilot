"""
Table extraction service using pdfplumber.

Converts detected tables into structured key-value text blocks
that can be embedded meaningfully into the RAG pipeline.
"""

from __future__ import annotations

import pdfplumber

from app.core.logging import logger


class TableService:
    """
    Extracts tables from a single PDF page (by page number)
    using pdfplumber and formats them as structured text.
    """

    def extract_from_page(self, pdf_path: str, page_number: int) -> tuple[str, int]:
        """
        Extract tables from a given page number (1-indexed).

        Returns:
            (table_text, table_count)
        """
        texts: list[str] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # pdfplumber uses 0-indexed pages
                page = pdf.pages[page_number - 1]
                tables = page.extract_tables()

                for table in tables:
                    if not table:
                        continue
                    text = self._table_to_text(table)
                    if text:
                        texts.append(text)

        except Exception as e:
            logger.warning(f"Table extraction failed on page {page_number}: {e}")

        return "\n\n".join(texts), len(texts)

    def _table_to_text(self, table: list[list]) -> str:
        """
        Converts a 2D table array into structured key-value text.

        If the first row looks like a header, uses header names as keys.
        Otherwise uses Column_N notation.
        """
        if not table or len(table) < 2:
            return ""

        rows = [[str(cell).strip() if cell is not None else "" for cell in row] for row in table]

        header = rows[0]
        data_rows = rows[1:]

        lines: list[str] = []
        for data_row in data_rows:
            # Skip blank rows
            if all(cell == "" for cell in data_row):
                continue
            entry_parts = []
            for i, cell in enumerate(data_row):
                col_name = header[i] if i < len(header) and header[i] else f"Column_{i + 1}"
                if cell:
                    entry_parts.append(f"{col_name}: {cell}")
            if entry_parts:
                lines.append("\n".join(entry_parts))

        return "\n\n".join(lines)
