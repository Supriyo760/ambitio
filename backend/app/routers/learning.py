from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..db import get_db
from .. import models
from ..services import edit_learner

router = APIRouter(prefix="/api/matters", tags=["learning"])

class EditRequest(BaseModel):
    draft_id: str
    original_text: str
    edited_text: str

@router.post("/{matter_id}/edits", response_model=dict)
def submit_edit(matter_id: str, req: EditRequest, db: Session = Depends(get_db)):
    rule = edit_learner.save_edit_and_extract_rule(
        db, 
        matter_id=matter_id, 
        draft_id=req.draft_id, 
        original_text=req.original_text, 
        edited_text=req.edited_text
    )
    
    return {
        "status": "success",
        "rule_extracted": rule is not None,
        "rule": {"id": rule.id, "description": rule.rule_text} if rule else None
    }

@router.get("/{matter_id}/rules", response_model=dict)
def list_rules(matter_id: str, db: Session = Depends(get_db)):
    rules = db.query(models.LearnedRule).filter(models.LearnedRule.matter_id == matter_id).all()
    results = []
    for r in rules:
        results.append({
            "id": r.id,
            "description": r.rule_text,
            "is_active": r.active,
            "created_at": r.created_at
        })
    return {"items": results}

class RuleToggleRequest(BaseModel):
    active: bool

@router.patch("/{matter_id}/rules/{rule_id}", response_model=dict)
def toggle_rule(matter_id: str, rule_id: str, req: RuleToggleRequest, db: Session = Depends(get_db)):
    rule = db.query(models.LearnedRule).filter(models.LearnedRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
        
    rule.active = req.active
    db.commit()
    return {
        "id": rule.id,
        "active": rule.active
    }
