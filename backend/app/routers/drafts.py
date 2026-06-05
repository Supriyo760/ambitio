from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..db import get_db
from .. import models, schemas
from ..services import draft_generator, grounding_checker

router = APIRouter(prefix="/api/matters", tags=["drafts"])

class DraftRequest(BaseModel):
    template_type: str = "Case Fact Summary"

@router.post("/{matter_id}/drafts/generate", response_model=dict)
def create_draft(matter_id: str, req: DraftRequest, db: Session = Depends(get_db)):
    result = draft_generator.generate_draft(db, matter_id, req.template_type)
    return result

class DraftSaveRequest(BaseModel):
    edited_markdown: str

@router.put("/{matter_id}/drafts/{draft_id}", response_model=dict)
def save_draft(matter_id: str, draft_id: str, req: DraftSaveRequest, db: Session = Depends(get_db)):
    draft = db.query(models.Draft).filter(models.Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
        
    draft.edited_markdown = req.edited_markdown
    draft.status = "EDITED"
    db.commit()
    
    return {
        "id": draft.id,
        "status": draft.status,
        "updated_at": draft.updated_at
    }

@router.get("/{matter_id}/drafts", response_model=dict)
def list_drafts(matter_id: str, db: Session = Depends(get_db)):
    drafts = db.query(models.Draft).filter(models.Draft.matter_id == matter_id).all()
    results = []
    for d in drafts:
        results.append({
            "id": d.id,
            "draft_type": d.draft_type,
            "status": d.status,
            "created_at": d.created_at
        })
    return {"items": results}

@router.get("/{matter_id}/drafts/{draft_id}", response_model=dict)
def get_draft(matter_id: str, draft_id: str, db: Session = Depends(get_db)):
    draft = db.query(models.Draft).filter(models.Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
        
    citations = db.query(models.Citation).filter(models.Citation.draft_id == draft_id).all()
    cit_list = []
    for c in citations:
        chunk = db.query(models.Chunk).filter(models.Chunk.id == c.chunk_id).first()
        cit_list.append({
            "id": c.evidence_id,
            "text": c.claim_text,
            "passage": chunk.text if chunk else ""
        })
        
    return {
        "id": draft.id,
        "draft_type": draft.draft_type,
        "generated_markdown": draft.generated_markdown,
        "status": draft.status,
        "citations": cit_list
    }

@router.post("/{matter_id}/drafts/{draft_id}/check", response_model=dict)
def check_draft_grounding(matter_id: str, draft_id: str, db: Session = Depends(get_db)):
    issues = grounding_checker.check_grounding(db, draft_id)
    return {"issues": issues}
