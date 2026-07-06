from pathlib import Path
from uuid import uuid4

import pandas as pd

from app.models.document import Document, Page
from app.utils.metadata import MetadataExtractor


class ExcelLoader:

    def load(self, excel_path: Path) -> Document:

        workbook = pd.read_excel(
            excel_path,
            sheet_name=None,
        )

        pages = []

        all_text = ""

        for index, (sheet, dataframe) in enumerate(workbook.items(), start=1):

            text = dataframe.to_string(index=False)

            all_text += text + "\n"

            pages.append(
                Page(
                    page_number=index,
                    text=f"Sheet: {sheet}\n\n{text}",
                )
            )

        metadata = MetadataExtractor().extract(
            excel_path.name,
            all_text,
        )

        return Document(
            document_id=str(uuid4()),
            filename=excel_path.name,
            total_pages=len(pages),
            domain=metadata["domain"],
            department=metadata["department"],
            document_type="Excel",
            metadata=metadata,
            pages=pages,
        )