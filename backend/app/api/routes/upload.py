import shutil

from fastapi import APIRouter, File, UploadFile

from app.core.config import UPLOAD_DIR
from app.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/api/v1/upload",
    tags=["Upload"],
)

service = IngestionService()


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return service.ingest_pdf(file_path)

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return service.ingest_image(file_path)