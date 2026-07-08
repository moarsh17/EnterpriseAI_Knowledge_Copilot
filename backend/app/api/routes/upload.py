from fastapi import APIRouter, UploadFile

from app.services.ingestion_service import IngestionService
from app.services.upload_service import UploadService

router = APIRouter(
    prefix="/api/v1/upload",
    tags=["Upload"],
)

upload_service = UploadService()
ingestion_service = IngestionService()


@router.post("/")
async def upload(file: UploadFile):
    try:
        file_path = await upload_service.save_file(file)
        result = ingestion_service.ingest(file_path)
        return {
            "filename": file.filename,
            "status": "success",
            "details": result,
        }
    except Exception as e:
        return {
            "filename": file.filename,
            "status": "error",
            "detail": str(e),
        }