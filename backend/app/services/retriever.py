from sqlalchemy.orm import Session
from .. import models
from . import vector_store

def retrieve_evidence(db: Session, matter_id: str, query: str, mode: str = "hybrid", top_k: int = 5):
    retrieved = []
    
    # 1. Semantic Search
    if mode in ["semantic", "hybrid"]:
        try:
            semantic_results = vector_store.semantic_search(matter_id, query, n_results=top_k * 2)
            for sr in semantic_results:
                retrieved.append({
                    "chunk_id": sr["chunk_id"],
                    "score": sr["score"],
                    "reason": "Semantic match"
                })
        except Exception as e:
            print(f"Vector search failed: {e}")
            
    # 2. Keyword Fallback (Simplistic implementation)
    if mode in ["keyword", "hybrid"]:
        keywords = query.lower().split()
        chunks = db.query(models.Chunk).filter(models.Chunk.matter_id == matter_id).all()
        for chunk in chunks:
            text_lower = chunk.text.lower()
            match_count = sum(1 for kw in keywords if kw in text_lower)
            if match_count > 0:
                score = match_count / len(keywords)
                retrieved.append({
                    "chunk_id": chunk.id,
                    "score": score,
                    "reason": f"Keyword match ({match_count}/{len(keywords)})"
                })
                
    # 3. Deduplicate and sort
    merged = {}
    for item in retrieved:
        cid = item["chunk_id"]
        if cid not in merged or item["score"] > merged[cid]["score"]:
            merged[cid] = item
            
    sorted_chunks = sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:top_k]
    
    # 4. Enrich with DB metadata
    evidence_items = []
    for idx, sc in enumerate(sorted_chunks):
        chunk_model = db.query(models.Chunk).filter(models.Chunk.id == sc["chunk_id"]).first()
        doc_model = db.query(models.Document).filter(models.Document.id == chunk_model.document_id).first()
        
        evidence_items.append({
            "evidence_id": f"E{idx + 1}",
            "chunk_id": chunk_model.id,
            "document_id": doc_model.id,
            "document_title": doc_model.filename,
            "page_number": chunk_model.page_start,
            "passage": chunk_model.text,
            "score": sc["score"],
            "confidence": chunk_model.confidence or 0.8,
            "reason": sc["reason"]
        })
        
    return evidence_items
