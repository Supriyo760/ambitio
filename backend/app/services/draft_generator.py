from sqlalchemy.orm import Session
from .. import models
from .llm_client import get_llm_client
from .retriever import retrieve_evidence

def generate_draft(db: Session, matter_id: str, template_type: str) -> dict:
    llm = get_llm_client()
    
    matter = db.query(models.Matter).filter(models.Matter.id == matter_id).first()
    fields = db.query(models.ExtractedField).filter(models.ExtractedField.matter_id == matter_id).all()
    rules = db.query(models.LearnedRule).filter(models.LearnedRule.matter_id == matter_id).all()
    
    # Simple semantic search to get all context for the matter
    # In a real system, we'd query specifically for the template parts
    evidence = retrieve_evidence(db, matter_id, "Summarize all key facts, dates, and money.", mode="semantic", top_k=10)
    
    facts_str = "\n".join([f"{f.field_name}: {f.value}" for f in fields])
    rules_str = "\n".join([f"Rule: {r.rule_text}" for r in rules])
    context_str = "\n".join([f"[{e['evidence_id']}] {e['passage']}" for e in evidence])
    
    sys_prompt = "You are an expert legal assistant drafting documents. Use the provided structured facts, style rules, and context."
    user_prompt = f"Template: {template_type}\n\nFacts:\n{facts_str}\n\nRules:\n{rules_str}\n\nContext:\n{context_str}\n\nDraft the document."
    
    try:
        content = llm.complete_text(sys_prompt, user_prompt)
    except Exception as e:
        content = f"Draft generation failed: {e}"
        
    # Save draft
    draft_model = models.Draft(
        matter_id=matter_id,
        draft_type=template_type,
        generated_markdown=content,
        status="DRAFT"
    )
    db.add(draft_model)
    db.commit()
    db.refresh(draft_model)
    
    # Save citations (Mocked for now, in reality LLM would return these or we parse them)
    # We just link to the evidence we retrieved
    for e in evidence:
        citation = models.Citation(
            draft_id=draft_model.id,
            matter_id=matter_id,
            evidence_id=e["evidence_id"],
            chunk_id=e["chunk_id"],
            claim_text=f"See {e['document_title']}, Page {e['page_number']}",
            section_name="Core Facts",
            confidence=1.0
        )
        db.add(citation)
        
    db.commit()
    
    return {
        "id": draft_model.id,
        "matter_id": draft_model.matter_id,
        "generated_markdown": draft_model.generated_markdown,
        "citations": [{"id": e["evidence_id"], "text": e["passage"]} for e in evidence]
    }
