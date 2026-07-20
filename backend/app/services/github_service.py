from uuid import uuid4
from app.loaders.github_loader import GithubLoader
from app.rag.ingestion import RAGIngestionPipeline
from app.rag.vectorstore import get_vectorstore
from app.core.logging import logger

class GithubService:
    def __init__(self):
        self.pipeline = RAGIngestionPipeline()
        self.loader = GithubLoader()
        self.vectorstore = get_vectorstore()

    def _check_duplicate(self, repo_url: str) -> str | None:
        docs = self.vectorstore.get(where={"repository_url": repo_url})
        if docs.get("metadatas") and len(docs["metadatas"]) > 0:
            return docs["metadatas"][0].get("document_id")
        return None

    def ingest_repo(self, repo_url: str) -> dict:
        existing_id = self._check_duplicate(repo_url)
        if existing_id:
            self.delete_repo(existing_id)
            
        repo_id = str(uuid4())
        
        target_dir = self.loader.clone_repo(repo_url, repo_id)
        repo_name = target_dir.name
        
        page_gen = self.loader.stream_pages(target_dir, repo_url)
        
        report = self.pipeline.ingest_streaming(
            page_generator=page_gen,
            document_id=repo_id,
            filename=repo_name,
            document_type="GitHub",
            domain="Code",
            department="Engineering",
            extra_metadata={
                "repository_name": repo_name,
                "repository_url": repo_url,
                "source_type": "github"
            }
        )
        
        return report

    def delete_repo(self, repo_id: str):
        docs = self.vectorstore.get(where={"document_id": repo_id})
        
        if docs.get("ids"):
            self.vectorstore.delete(ids=docs["ids"])
            
        from app.core.config import UPLOAD_DIR
        import shutil
        
        target_dir = UPLOAD_DIR / "github_repos" / repo_id
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
            
        from app.rag.memory import clear_memory
        clear_memory()

    def sync_repo(self, repo_id: str) -> dict:
        docs = self.vectorstore.get(where={"document_id": repo_id})
        metadatas = docs.get("metadatas", [])
        if not metadatas:
            raise ValueError("Repository not found")
            
        repo_url = metadatas[0].get("repository_url")
        if not repo_url:
            raise ValueError("Repository URL missing in metadata")
            
        return self.ingest_repo(repo_url)

    def get_indexed_repos(self) -> list[dict]:
        docs = self.vectorstore.get(where={"source_type": "github"})
        metadatas = docs.get("metadatas", [])
        
        unique_repos = {}
        for meta in metadatas:
            doc_id = meta.get("document_id")
            if doc_id and doc_id not in unique_repos:
                unique_repos[doc_id] = {
                    "document_id": doc_id,
                    "repository_name": meta.get("repository_name"),
                    "repository_url": meta.get("repository_url")
                }
        return list(unique_repos.values())
