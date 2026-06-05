import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

from sqlalchemy.orm import Session
from . import chunker
from .. import models

# Function to extract text from a single page using PyMuPDF
def extract_text_pymupdf(page: fitz.Page) -> str:
    text = page.get_text("text")
    return text.strip() if text else ""

# Function to extract text from an image using pytesseract
def extract_text_ocr(image_bytes: bytes) -> tuple[str, float]:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # For simplicity, we just use image_to_data to get confidence, or image_to_string
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        text_parts = []
        confidences = []
        
        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            conf = int(data['conf'][i])
            if word and conf != -1:
                text_parts.append(word)
                confidences.append(conf)
                
        full_text = " ".join(text_parts)
        avg_conf = sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
        return full_text, avg_conf
    except Exception as e:
        return "", 0.0

def process_document(db: Session, document: models.Document):
    file_path = document.storage_path
    file_ext = document.file_type.lower()
    
    warnings = []
    total_pages = 0
    all_chunks = []
    
    if file_ext == '.txt':
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        total_pages = 1
        page_model = models.Page(
            document_id=document.id,
            matter_id=document.matter_id,
            page_number=1,
            text=text,
            extraction_method="digital_text",
            confidence=1.0,
            warnings_json=[]
        )
        db.add(page_model)
        
        chunks = chunker.chunk_text(text)
        for c in chunks:
            all_chunks.append({
                "page_start": 1,
                "page_end": 1,
                "text": c,
                "extraction_method": "digital_text",
                "confidence": 1.0
            })
            
    elif file_ext == '.pdf':
        doc = fitz.open(file_path)
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            text = extract_text_pymupdf(page)
            
            method = "digital_text"
            confidence = 1.0
            page_warnings = []
            
            if len(text) < 50:  # arbitrary threshold for OCR fallback
                # Extract image of the page and OCR it
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                ocr_text, ocr_conf = extract_text_ocr(img_bytes)
                
                if len(ocr_text) > len(text):
                    text = ocr_text
                    method = "ocr"
                    confidence = ocr_conf
                    if confidence < 0.75:
                        page_warnings.append(f"Low OCR confidence ({confidence:.2f}) on page {page_num + 1}")
            
            page_model = models.Page(
                document_id=document.id,
                matter_id=document.matter_id,
                page_number=page_num + 1,
                text=text,
                extraction_method=method,
                confidence=confidence,
                warnings_json=page_warnings
            )
            db.add(page_model)
            warnings.extend(page_warnings)
            
            chunks = chunker.chunk_text(text)
            for c in chunks:
                all_chunks.append({
                    "page_start": page_num + 1,
                    "page_end": page_num + 1,
                    "text": c,
                    "extraction_method": method,
                    "confidence": confidence
                })
        doc.close()
    
    # Process chunks
    from . import vector_store
    chunk_data_for_vector = []
    
    for c_data in all_chunks:
        c_text = c_data["text"]
        c_hash = chunker.generate_text_hash(c_text)
        chunk_model = models.Chunk(
            matter_id=document.matter_id,
            document_id=document.id,
            page_start=c_data["page_start"],
            page_end=c_data["page_end"],
            text=c_text,
            text_hash=c_hash,
            extraction_method=c_data["extraction_method"],
            confidence=c_data["confidence"]
        )
        db.add(chunk_model)
        db.flush() # flush to get the id if needed, or we can use a temporary id, actually sqlite generates it after commit, but let's commit later.
        
        # We need an id for vector store. SQLite assigns id after commit.
        # Let's commit chunks first.
        
    db.commit()
    
    # Now push to vector store
    for chunk_model in db.query(models.Chunk).filter(models.Chunk.document_id == document.id).all():
        chunk_data_for_vector.append({
            "chunk_id": chunk_model.id,
            "text": chunk_model.text,
            "document_id": chunk_model.document_id,
            "page_number": chunk_model.page_start,
            "confidence": chunk_model.confidence
        })
        
    if chunk_data_for_vector:
        vector_store.add_chunks_to_vector_store(document.matter_id, chunk_data_for_vector)
        
    document.page_count = total_pages
    document.status = "READY"
    document.warnings_json = warnings
    db.commit()
