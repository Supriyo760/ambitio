import re
from sqlalchemy.orm import Session
from .. import models
from .llm_client import get_llm_client

def extract_structured_fields(db: Session, matter_id: str):
    llm = get_llm_client()
    
    chunks = db.query(models.Chunk).filter(models.Chunk.matter_id == matter_id).all()
    
    date_pattern = r'\b(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[a-z\s,.]*\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b'
    money_pattern = r'(?:Rs\.?|INR|\$|USD)\s*[\d,]+(?:\.\d{2})?'
    party_pattern = r'\b(?:Mr\.|Mrs\.|Ms\.|M/s\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b'
    
    for c in chunks:
        # Regex extraction
        dates = set(re.findall(date_pattern, c.text, re.IGNORECASE))
        for d in dates:
            save_field(db, matter_id, c.document_id, c.id, "Date", "date", d, c.text, 0.95, c.page_start)
            
        moneys = set(re.findall(money_pattern, c.text, re.IGNORECASE))
        for m in moneys:
            save_field(db, matter_id, c.document_id, c.id, "Money", "currency", m, c.text, 0.90, c.page_start)

        parties = set(re.findall(party_pattern, c.text))
        for p in parties:
            save_field(db, matter_id, c.document_id, c.id, "Party", "string", p, c.text, 0.85, c.page_start)
            
        # Mock LLM Extraction
        try:
            res = llm.complete_json("Extract structured facts: Party, Date, Money, Obligation, Notice, Address, Case Number.", c.text, {})
            if "fields" in res:
                for f in res["fields"]:
                    save_field(db, matter_id, c.document_id, c.id, f["field_name"], f["field_type"], f["value"], c.text, f.get("confidence", 0.8), c.page_start)
        except Exception as e:
            print(f"LLM extraction failed for chunk {c.id}: {e}")

def save_field(db, matter_id, document_id, chunk_id, name, f_type, value, text, conf, page_number):
    # Avoid exact duplicates
    existing = db.query(models.ExtractedField).filter(
        models.ExtractedField.matter_id == matter_id,
        models.ExtractedField.field_name == name,
        models.ExtractedField.value == value
    ).first()
    if not existing:
        f = models.ExtractedField(
            matter_id=matter_id,
            document_id=document_id,
            chunk_id=chunk_id,
            field_name=name,
            field_type=f_type,
            value=value,
            raw_text=text[:200] + "..." if len(text) > 200 else text,
            confidence=conf,
            page_number=page_number,
            status="NEEDS_REVIEW" if conf < 0.85 else "ACCEPTED"
        )
        db.add(f)
        db.commit()
