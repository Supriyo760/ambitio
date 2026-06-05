import pytest
from app.services.llm_client import MockLLMClient

def test_mock_llm_generates_8_sections():
    """Verify the mock LLM returns all 8 required sections."""
    llm = MockLLMClient()
    result = llm.complete_text(
        "You are a legal assistant.",
        "Template: Case Fact Summary\n\nFacts:\nDate: 2024-03-12\n\nRules:\n\nContext:\n[E1] Some context\n\nDraft the document."
    )
    assert "## 1. Matter Overview" in result
    assert "## 2. Parties Involved" in result
    assert "## 3. Key Dates and Events" in result
    assert "## 4. Documents Reviewed" in result
    assert "## 5. Core Facts" in result
    assert "## 6. Open Issues" in result
    assert "## 7. Evidence Table" in result
    assert "## 8. Suggested Next Steps" in result

def test_mock_llm_includes_citation_chips():
    """Verify the mock LLM output contains citation chips like [E1]."""
    llm = MockLLMClient()
    result = llm.complete_text(
        "You are a legal assistant.",
        "Template: Case Fact Summary\n\nFacts:\n\nRules:\n\nContext:\n\nDraft the document."
    )
    assert "[E1]" in result
    assert "[E2]" in result
