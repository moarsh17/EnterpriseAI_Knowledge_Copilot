from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import UPLOAD_DIR
from app.core.constants import SUPPORTED_FILE_TYPES


class UploadService:

    def validate_file(self, file: UploadFile):

        extension = Path(file.filename).suffix.lower()

        if extension not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {extension}")

        return extension

    def generate_filename(self, original_name: str):

        extension = Path(original_name).suffix.lower()

        return f"{uuid4()}{extension}"

    async def save_file(self, file: UploadFile) -> Path:

        self.validate_file(file)

        filename = self.generate_filename(file.filename)

        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return file_path