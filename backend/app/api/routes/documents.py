from fastapi import APIRouter, HTTPException
from app.rag.vectorstore import get_vectorstore
from app.core.config import UPLOAD_DIR
from app.rag.memory import memory
import os

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)

@router.get("/")
def list_documents():
    try:
        vectorstore = get_vectorstore()
        docs = vectorstore.get()
        metadatas = docs.get("metadatas", [])
        
        unique_docs = {}
        for meta in metadatas:
            doc_id = meta.get("document_id")
            if doc_id and doc_id not in unique_docs:
                unique_docs[doc_id] = {
                    "document_id": doc_id,
                    "filename": meta.get("filename", "Unknown"),
                    "domain": meta.get("domain", "General"),
                    "department": meta.get("department", "General"),
                    "document_type": meta.get("document_type", "Unknown")
                }
        
        return list(unique_docs.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
def delete_document(document_id: str):
    try:
        vectorstore = get_vectorstore()
        
        # Fetch metadata to find the filename
        docs = vectorstore.get(where={"document_id": document_id})
        
        if not docs.get("ids"):
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found.")
            
        metadatas = docs.get("metadatas", [])
        if metadatas and len(metadatas) > 0:
            filename = metadatas[0].get("filename")
            if filename:
                file_path = UPLOAD_DIR / filename
                if file_path.exists():
                    os.remove(file_path)
                    
        # Delete vectors using standard ids list
        vectorstore.delete(ids=docs["ids"])
        
        # Clear conversational memory cache
        memory.clear()
        
        return {"status": "success", "message": f"Document {document_id} deleted."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
