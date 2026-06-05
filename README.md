# Grounded Legal Drafting Assistant

This project is the implementation of the Ambitio AI Intern Assessment. It is a full-stack web application designed to process messy legal documents, extract structured facts, retrieve evidence, generate a grounded draft memo, and learn from operator edits.

## Tech Stack
- **Frontend**: React + Vite + TypeScript
- **Backend**: FastAPI + Python
- **Database**: SQLite (SQLAlchemy)
- **Vector Store**: ChromaDB (Local persistent)
- **Document Processing**: PyMuPDF (digital), pytesseract (OCR fallback)

## Setup Instructions

### 1. Backend Setup
1. Open a terminal and navigate to the `backend/` directory.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. (Optional) Install Tesseract OCR if you want to test OCR fallback.
6. Start the server: `uvicorn app.main:app --reload --port 8000`

### 2. Frontend Setup
1. Open a new terminal and navigate to the `frontend/` directory.
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
4. Open `http://localhost:5173` in your browser.

## How to use
1. Navigate to the Matter Workspace and create a matter.
2. Go to the Documents tab and upload files (use `sample_data/inputs/`).
3. Click "Process All".
4. Review extracted text and pages in Document Review.
5. Review structured facts in Extracted Facts.
6. Test retrieval in Evidence Retrieval.
7. Generate a draft in Draft Generation.
8. Edit the draft and click Save Edit to generate a Learned Rule.
9. Review Learned Rules in the Edit Learning tab.

## Configuration
Copy `.env.example` to `.env` to configure the LLM provider (default is `mock`).
