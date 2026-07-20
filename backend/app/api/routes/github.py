from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.github_service import GithubService

router = APIRouter(
    prefix="/api/v1/github",
    tags=["GitHub"],
)

service = GithubService()

class GithubIngestRequest(BaseModel):
    repo_url: str

@router.post("/")
def ingest_github(request: GithubIngestRequest):
    try:
        report = service.ingest_repo(request.repo_url)
        return {"status": "success", "details": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_indexed_repos():
    try:
        repos = service.get_indexed_repos()
        return repos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{repo_id}")
def delete_repo(repo_id: str):
    try:
        service.delete_repo(repo_id)
        return {"status": "success", "message": f"Repository {repo_id} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{repo_id}/sync")
def sync_repo(repo_id: str):
    try:
        report = service.sync_repo(repo_id)
        return {"status": "success", "details": report}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
