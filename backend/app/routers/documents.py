from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os
import shutil

from ..db import get_db
from .. import models, schemas
from ..services import document_processor

router = APIRouter(prefix="/api/matters", tags=["documents"])

class ProcessRequest(BaseModel):
    document_ids: List[str]
    force_reprocess: bool = False

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{matter_id}/process", response_model=dict)
def process_documents(matter_id: str, req: ProcessRequest, db: Session = Depends(get_db)):
    matter = db.query(models.Matter).filter(models.Matter.id == matter_id).first()
    if not matter:
        raise HTTPException(status_code=404, detail="Matter not found")
        
    docs = db.query(models.Document).filter(
        models.Document.matter_id == matter_id,
        models.Document.id.in_(req.document_ids)
    ).all()
    
    warnings = []
    processed_count = 0
    
    for doc in docs:
        if doc.status == "READY" and not req.force_reprocess:
            continue
            
        doc.status = "PROCESSING"
        db.commit()
        
        # In a real app this would be a background task
        try:
            document_processor.process_document(db, doc)
            processed_count += 1
            if doc.warnings_json:
                warnings.extend(doc.warnings_json)
        except Exception as e:
            doc.status = "FAILED"
            doc.warnings_json = [str(e)]
            db.commit()
            warnings.append(f"Failed to process {doc.filename}: {str(e)}")
            
    # Run extraction for the matter
    from ..services import structured_extractor
    structured_extractor.extract_structured_fields(db, matter_id)
            
    matter.status = "READY_FOR_DRAFT"
    db.commit()
    
    return {
        "matter_id": matter_id,
        "status": "READY_FOR_DRAFT",
        "processed_documents": processed_count,
        "warnings": warnings
    }

@router.post("/{matter_id}/documents", response_model=dict)
def upload_documents(matter_id: str, files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    matter = db.query(models.Matter).filter(models.Matter.id == matter_id).first()
    if not matter:
        raise HTTPException(status_code=404, detail="Matter not found")
        
    uploaded_docs = []
    
    for file in files:
        # Save file to disk
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in [".txt", ".pdf", ".png", ".jpg", ".jpeg"]:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
            
        doc_model = models.Document(
            matter_id=matter_id,
            filename=file.filename,
            file_type=file_ext,
            storage_path="" # Temporary
        )
        db.add(doc_model)
        db.commit()
        db.refresh(doc_model)
        
        # Now create path
        matter_dir = os.path.join(UPLOAD_DIR, matter_id, doc_model.id)
        os.makedirs(matter_dir, exist_ok=True)
        file_path = os.path.join(matter_dir, "original" + file_ext)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        doc_model.storage_path = file_path
        db.commit()
        db.refresh(doc_model)
        
        uploaded_docs.append({
            "id": doc_model.id,
            "filename": doc_model.filename,
            "status": doc_model.status
        })
        
    return {"uploaded": uploaded_docs}

@router.get("/{matter_id}/documents", response_model=dict)
def list_documents(matter_id: str, db: Session = Depends(get_db)):
    docs = db.query(models.Document).filter(models.Document.matter_id == matter_id).all()
    results = []
    for d in docs:
        results.append({
            "id": d.id,
            "filename": d.filename,
            "status": d.status,
            "page_count": d.page_count,
            "extraction_method": d.extraction_method,
            "average_confidence": d.average_confidence,
            "warnings": d.warnings_json or []
        })
    return {"items": results}

@router.get("/{matter_id}/documents/{document_id}/pages", response_model=dict)
def get_document_pages(matter_id: str, document_id: str, db: Session = Depends(get_db)):
    pages = db.query(models.Page).filter(models.Page.document_id == document_id).order_by(models.Page.page_number).all()
    results = []
    for p in pages:
        results.append({
            "id": p.id,
            "page_number": p.page_number,
            "text": p.text,
            "extraction_method": p.extraction_method,
            "confidence": p.confidence,
            "warnings": p.warnings_json or []
        })
    return {"items": results}
