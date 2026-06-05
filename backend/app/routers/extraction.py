from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..services import structured_extractor

router = APIRouter(prefix="/api/matters", tags=["extraction"])

@router.post("/{matter_id}/extract", response_model=dict)
def run_extraction(matter_id: str, db: Session = Depends(get_db)):
    structured_extractor.extract_structured_fields(db, matter_id)
    return {"status": "success", "matter_id": matter_id}

@router.get("/{matter_id}/fields", response_model=dict)
def list_extracted_fields(matter_id: str, db: Session = Depends(get_db)):
    fields = db.query(models.ExtractedField).filter(models.ExtractedField.matter_id == matter_id).all()
    results = []
    for f in fields:
        results.append({
            "id": f.id,
            "field_name": f.field_name,
            "field_type": f.field_type,
            "value": f.value,
            "raw_text": f.raw_text,
            "confidence": f.confidence,
            "document_id": f.document_id,
            "page_number": f.page_number,
            "chunk_id": f.chunk_id,
            "status": f.status,
            "needs_review": f.status == "NEEDS_REVIEW"
        })
    return {"items": results}
