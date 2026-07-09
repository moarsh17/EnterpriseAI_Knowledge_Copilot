import os
import shutil
from pathlib import Path
from typing import Generator
from git import Repo
from urllib.parse import urlparse

from app.models.document import Page
from app.core.config import UPLOAD_DIR
from app.core.logging import logger

class GithubLoader:
    def __init__(self):
        self.ignored_dirs = {
            ".git", "node_modules", "dist", "build", ".next", 
            "venv", "__pycache__", "target", "bin", "obj", ".idea", ".vscode"
        }
        self.supported_extensions = {
            ".py", ".js", ".ts", ".tsx", ".java", ".c", ".cpp", 
            ".h", ".go", ".md", ".json", ".yaml", ".yml", ".html", ".css"
        }

    def clone_repo(self, repo_url: str, repo_id: str) -> Path:
        repo_name = urlparse(repo_url).path.strip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
            
        target_dir = UPLOAD_DIR / "github_repos" / repo_id / repo_name
        
        if target_dir.exists():
            shutil.rmtree(target_dir)
            
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Cloning {repo_url} into {target_dir}")
        Repo.clone_from(repo_url, target_dir)
        return target_dir

    def stream_pages(self, target_dir: Path, repo_url: str) -> Generator[Page, None, None]:
        page_num = 1
        
        for root, _, files in os.walk(target_dir):
            for file in files:
                file_path = Path(root) / file
                
                # Check if file is valid
                if file_path.suffix.lower() not in self.supported_extensions:
                    continue
                    
                rel_path = file_path.relative_to(target_dir)
                is_valid = True
                for part in rel_path.parts:
                    if part in self.ignored_dirs:
                        is_valid = False
                        break
                        
                if not is_valid:
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    if not content.strip():
                        continue
                        
                    yield Page(
                        page_number=page_num,
                        text=content,
                        metadata={
                            "filename": file,
                            "file_path": str(rel_path).replace("\\", "/"),
                            "repository_url": repo_url,
                            "source_type": "github"
                        }
                    )
                    page_num += 1
                except UnicodeDecodeError:
                    pass
                except Exception as e:
                    logger.warning(f"Error reading {file_path}: {e}")
