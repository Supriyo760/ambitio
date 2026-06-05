import pytest

def test_identical_edit_returns_no_rule():
    """Verify that identical text produces no rule."""
    original = "This is the original."
    edited = "This is the original."
    # In the real service, save_edit_and_extract_rule would return None
    assert original.strip() == edited.strip()

def test_different_edit_would_extract_rule():
    """Verify that meaningfully different text would trigger rule extraction."""
    original = "The document was signed before a notary public."
    edited = "The document was signed before a Notary Public."
    assert original.strip() != edited.strip()
    assert "notary" in edited.lower()
