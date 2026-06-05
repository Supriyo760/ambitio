from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..db import get_db
from .. import models

router = APIRouter(prefix="/api/evaluation", tags=["evaluation"])

class EvaluationRequest(BaseModel):
    sample_set: str = "default"

@router.post("/run", response_model=dict)
def run_evaluation(req: EvaluationRequest, db: Session = Depends(get_db)):
    # Mocking evaluation run as per MVP instructions
    
    metrics = {
        "documents_processed": 3,
        "pages_processed": 3,
        "ocr_fallback_pages": 1,
        "structured_fields_expected": 12,
        "structured_fields_found": 10,
        "field_recall": 0.83,
        "retrieval_precision_at_5": 0.80,
        "citation_coverage": 0.90,
        "unsupported_claim_count": 0,
        "learned_rules_created": 3,
        "learned_rules_applied": 1
    }
    
    results_markdown = """## Evaluation Results
    
- **Extraction Completeness**: The system correctly extracted 10 out of 12 fields (83% recall).
- **Retrieval Relevance**: Precision at top 5 chunks is 80%.
- **Grounding**: 90% of factual claims in the draft are correctly cited. Unsupported claim count is 0.
- **Edit Learning**: Extracted 3 rules from operator edits, with 1 applied automatically to the subsequent draft.

*Note: These are simulated evaluation metrics for the MVP.*
"""
    
    eval_run = models.EvaluationRun(
        name=f"Eval Run - {req.sample_set}",
        metrics_json=metrics,
        results_markdown=results_markdown
    )
    db.add(eval_run)
    db.commit()
    db.refresh(eval_run)
    
    return {
        "id": eval_run.id,
        "metrics": metrics,
        "results_markdown": results_markdown
    }
