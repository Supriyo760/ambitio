import pytest
from app.services.chunker import chunk_text

def test_chunk_text():
    text = "This is a simple sentence. " * 50  # Roughly 1350 chars
    chunks = chunk_text(text, max_length=1000, overlap=200)
    
    assert len(chunks) > 1
    assert len(chunks[0]) <= 1000
    # Check overlap (roughly)
    assert chunks[0][-100:] in chunks[1]
