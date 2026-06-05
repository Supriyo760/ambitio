from sqlalchemy.orm import Session
from .. import models
from .llm_client import get_llm_client

def check_grounding(db: Session, draft_id: str) -> list[dict]:
    llm = get_llm_client()
    draft = db.query(models.Draft).filter(models.Draft.id == draft_id).first()
    citations = db.query(models.Citation).filter(models.Citation.draft_id == draft_id).all()
    
    # Simplistic mock of a grounding check
    issues = []
    
    if not citations:
        issues.append({
            "severity": "high",
            "message": "Draft contains no citations.",
            "context": None
        })
        return issues
        
    for cit in citations:
        chunk = db.query(models.Chunk).filter(models.Chunk.id == cit.chunk_id).first()
        
        # Ask LLM if the citation supports the draft
        sys = "Check if the source supports the claim."
        user = f"Source: {chunk.text}\nClaim: {draft.generated_markdown[:200]}..." # Very simplified
        
        # In our mock, just randomly pass or fail, or we can just assume pass
        issues.append({
            "severity": "low",
            "message": f"Citation {cit.id} needs review.",
            "context": chunk.text
        })
        
    return issues
