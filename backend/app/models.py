from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
import datetime
import uuid

from .db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Matter(Base):
    __tablename__ = "matters"
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="EMPTY")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=generate_uuid)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    status = Column(String, default="UPLOADED")
    page_count = Column(Integer, default=0)
    extraction_method = Column(String, nullable=True)
    average_confidence = Column(Float, nullable=True)
    warnings_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Page(Base):
    __tablename__ = "pages"
    id = Column(String, primary_key=True, default=generate_uuid)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)
    extraction_method = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    warnings_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(String, primary_key=True, default=generate_uuid)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    page_start = Column(Integer, nullable=False)
    page_end = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    text_hash = Column(String, nullable=False)
    token_count = Column(Integer, nullable=True)
    extraction_method = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ExtractedField(Base):
    __tablename__ = "extracted_fields"
    id = Column(String, primary_key=True, default=generate_uuid)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    chunk_id = Column(String, ForeignKey("chunks.id"), nullable=False)
    field_name = Column(String, nullable=False)
    field_type = Column(String, nullable=False)
    value = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False)
    page_number = Column(Integer, nullable=True)
    status = Column(String, default="ACCEPTED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Draft(Base):
    __tablename__ = "drafts"
    id = Column(String, primary_key=True, default=generate_uuid)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    draft_type = Column(String, nullable=False)
    status = Column(String, default="GENERATING")
    generated_markdown = Column(Text, nullable=True)
    edited_markdown = Column(Text, nullable=True)
    citation_coverage = Column(Float, nullable=True)
    unsupported_claim_count = Column(Integer, nullable=True)
    warnings_json = Column(JSON, nullable=True)
    applied_rule_ids_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Citation(Base):
    __tablename__ = "citations"
    id = Column(String, primary_key=True, default=generate_uuid)
    draft_id = Column(String, ForeignKey("drafts.id"), nullable=False)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    evidence_id = Column(String, nullable=False)
    chunk_id = Column(String, ForeignKey("chunks.id"), nullable=False)
    claim_text = Column(Text, nullable=False)
    section_name = Column(String, nullable=False)
    support_reason = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OperatorEdit(Base):
    __tablename__ = "operator_edits"
    id = Column(String, primary_key=True, default=generate_uuid)
    draft_id = Column(String, ForeignKey("drafts.id"), nullable=False)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=False)
    original_markdown = Column(Text, nullable=False)
    edited_markdown = Column(Text, nullable=False)
    diff_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LearnedRule(Base):
    __tablename__ = "learned_rules"
    id = Column(String, primary_key=True, default=generate_uuid)
    matter_id = Column(String, ForeignKey("matters.id"), nullable=True)
    category = Column(String, nullable=False)
    scope = Column(String, nullable=False)
    rule_text = Column(Text, nullable=False)
    example_before = Column(Text, nullable=True)
    example_after = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    source_edit_id = Column(String, ForeignKey("operator_edits.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"
    id = Column(String, primary_key=True, default=generate_uuid)
    matter_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    metrics_json = Column(JSON, nullable=True)
    results_markdown = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
