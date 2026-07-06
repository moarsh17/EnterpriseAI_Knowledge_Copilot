from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ingestion_service import IngestionService
from app.services.upload_service import UploadService

router = APIRouter(
    prefix="/api/v1/upload",
    tags=["Upload"],
)

upload_service = UploadService()
ingestion_service = IngestionService()


@router.post("/")
async def upload(file: UploadFile = File(...)):

    try:

        file_path = await upload_service.save_file(file)

        return ingestion_service.ingest(file_path)

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )