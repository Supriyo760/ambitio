from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/matters", tags=["matters"])

@router.post("", response_model=schemas.MatterResponse)
def create_matter(matter: schemas.MatterCreate, db: Session = Depends(get_db)):
    db_matter = models.Matter(title=matter.title, description=matter.description)
    db.add(db_matter)
    db.commit()
    db.refresh(db_matter)
    
    # Calculate document_count for response
    db_matter.document_count = 0
    return db_matter

@router.get("", response_model=dict)
def list_matters(db: Session = Depends(get_db)):
    matters = db.query(models.Matter).all()
    results = []
    for m in matters:
        doc_count = db.query(models.Document).filter(models.Document.matter_id == m.id).count()
        results.append({
            "id": m.id,
            "title": m.title,
            "status": m.status,
            "document_count": doc_count,
            "updated_at": m.updated_at
        })
    return {"items": results}

@router.get("/{matter_id}", response_model=dict)
def get_matter(matter_id: str, db: Session = Depends(get_db)):
    matter = db.query(models.Matter).filter(models.Matter.id == matter_id).first()
    if not matter:
        raise HTTPException(status_code=404, detail="Matter not found")
        
    doc_count = db.query(models.Document).filter(models.Document.matter_id == matter_id).count()
    page_count = db.query(models.Page).filter(models.Page.matter_id == matter_id).count()
    chunk_count = db.query(models.Chunk).filter(models.Chunk.matter_id == matter_id).count()
    extracted_fields = db.query(models.ExtractedField).filter(models.ExtractedField.matter_id == matter_id).count()
    drafts = db.query(models.Draft).filter(models.Draft.matter_id == matter_id).count()
    learned_rules = db.query(models.LearnedRule).filter(models.LearnedRule.matter_id == matter_id).count()
    
    return {
        "id": matter.id,
        "title": matter.title,
        "status": matter.status,
        "summary": {
            "documents": doc_count,
            "pages": page_count,
            "chunks": chunk_count,
            "extracted_fields": extracted_fields,
            "drafts": drafts,
            "learned_rules": learned_rules
        }
    }

@router.delete("/{matter_id}")
def delete_matter(matter_id: str, db: Session = Depends(get_db)):
    matter = db.query(models.Matter).filter(models.Matter.id == matter_id).first()
    if not matter:
        raise HTTPException(status_code=404, detail="Matter not found")
        
    # Manual cascade delete to avoid orphans
    db.query(models.LearnedRule).filter(models.LearnedRule.matter_id == matter_id).delete()
    db.query(models.OperatorEdit).filter(models.OperatorEdit.matter_id == matter_id).delete()
    db.query(models.Citation).filter(models.Citation.matter_id == matter_id).delete()
    db.query(models.Draft).filter(models.Draft.matter_id == matter_id).delete()
    db.query(models.ExtractedField).filter(models.ExtractedField.matter_id == matter_id).delete()
    db.query(models.Chunk).filter(models.Chunk.matter_id == matter_id).delete()
    db.query(models.Page).filter(models.Page.matter_id == matter_id).delete()
    db.query(models.Document).filter(models.Document.matter_id == matter_id).delete()
    
    db.delete(matter)
    db.commit()
    return {"status": "success"}
