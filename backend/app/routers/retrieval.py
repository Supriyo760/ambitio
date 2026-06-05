from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from ..db import get_db
from ..services import retriever

router = APIRouter(prefix="/api/matters", tags=["retrieval"])

class SearchQuery(BaseModel):
    query: str
    mode: str = "hybrid" # semantic, keyword, hybrid
    top_k: int = 5

@router.post("/{matter_id}/search", response_model=dict)
def search_evidence(matter_id: str, search: SearchQuery, db: Session = Depends(get_db)):
    results = retriever.retrieve_evidence(
        db,
        matter_id=matter_id,
        query=search.query,
        mode=search.mode,
        top_k=search.top_k
    )
    
    return {
        "query": search.query,
        "results": results
    }
