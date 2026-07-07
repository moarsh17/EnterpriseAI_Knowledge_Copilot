from typing import List
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
async def upload(files: List[UploadFile] = File(...)):
    results = []
    errors = []

    for file in files:
        try:
            file_path = await upload_service.save_file(file)
            result = ingestion_service.ingest(file_path)
            results.append({
                "filename": file.filename,
                "status": "success",
                "details": result
            })
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "status": "error",
                "detail": str(e)
            })

    return {
        "results": results,
        "errors": errors
    }