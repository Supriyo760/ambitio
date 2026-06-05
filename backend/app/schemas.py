from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MatterBase(BaseModel):
    title: str
    description: Optional[str] = None

class MatterCreate(MatterBase):
    pass

class MatterResponse(MatterBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    document_count: Optional[int] = None

    class Config:
        orm_mode = True

class DocumentResponse(BaseModel):
    id: str
    matter_id: str
    filename: str
    file_type: str
    status: str
    page_count: int
    extraction_method: Optional[str] = None
    average_confidence: Optional[float] = None
    warnings: Optional[List[str]] = None

    class Config:
        orm_mode = True

class ExtractedFieldResponse(BaseModel):
    id: str
    field_name: str
    field_type: str
    value: Optional[str]
    raw_text: Optional[str]
    confidence: float
    document_id: str
    page_number: Optional[int]
    chunk_id: str
    status: str

    class Config:
        orm_mode = True

class EvidenceItem(BaseModel):
    evidence_id: str
    chunk_id: str
    document_id: str
    document_title: str
    page_number: int
    passage: str
    score: float
    confidence: float
    reason: Optional[str]

class DraftGenerateRequest(BaseModel):
    draft_type: str = "case_fact_summary_internal_memo"
    apply_learned_rules: bool = True

class CitationResponse(BaseModel):
    id: str
    evidence_id: str
    claim_text: str
    chunk_id: str
    section_name: str
    support_reason: Optional[str]
    confidence: float

    class Config:
        orm_mode = True

class DraftResponse(BaseModel):
    id: str
    matter_id: str
    status: str
    generated_markdown: Optional[str]
    edited_markdown: Optional[str]
    citation_coverage: Optional[float]
    unsupported_claim_count: Optional[int]
    warnings: Optional[List[str]]
    citations: Optional[List[CitationResponse]] = []
    applied_rules: Optional[List[str]] = []

    class Config:
        orm_mode = True

class EditSubmitRequest(BaseModel):
    edited_markdown: str

class LearnedRuleResponse(BaseModel):
    id: str
    category: str
    scope: str
    rule_text: str
    confidence: float
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class RuleToggleRequest(BaseModel):
    active: bool
