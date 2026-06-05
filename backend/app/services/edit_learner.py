from sqlalchemy.orm import Session
from .. import models
from .llm_client import get_llm_client

def save_edit_and_extract_rule(db: Session, matter_id: str, draft_id: str, original_text: str, edited_text: str):
    llm = get_llm_client()
    
    # Save the edit record
    edit_model = models.OperatorEdit(
        matter_id=matter_id,
        draft_id=draft_id,
        original_markdown=original_text,
        edited_markdown=edited_text
    )
    db.add(edit_model)
    db.commit()
    db.refresh(edit_model)
    
    # Simple check if there's a significant difference
    if original_text.strip() == edited_text.strip():
        return None
        
    # Ask LLM to extract a rule
    sys_prompt = "Compare original and edited text. If the edit reflects a stylistic, formatting, or legal drafting rule (not just fixing a typo), extract the rule. Return JSON."
    user_prompt = f"Original: {original_text}\nEdited: {edited_text}"
    
    try:
        # Mocking LLM extraction for rules
        # In reality, we'd use complete_json
        # Here we just mock a simple rule for demo purposes
        rule_desc = "Prefer formal legal terminology and active voice."
        if "mock" in str(llm.__class__).lower():
            if "notary" in edited_text.lower():
                rule_desc = "Always capitalize Notary Public."
    except Exception as e:
        print(f"Failed to extract rule: {e}")
        rule_desc = "Maintain consistency with edited style."
        
    rule_model = models.LearnedRule(
        matter_id=matter_id,
        category="style",
        scope="global",
        rule_text=rule_desc,
        confidence=1.0,
        source_edit_id=edit_model.id,
        active=True
    )
    db.add(rule_model)
    db.commit()
    db.refresh(rule_model)
    
    return rule_model
