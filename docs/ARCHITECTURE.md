# System Architecture

## Overview
The Grounded Legal Drafting Assistant is built with a decoupled frontend and backend.

- **Frontend**: React (Vite) + TypeScript. Uses React Router for navigation. Communicates via REST.
- **Backend**: FastAPI + SQLAlchemy (SQLite) + ChromaDB.

## Core Modules
1. **Document Processor**: Orchestrates PyMuPDF text extraction and PyTesseract OCR.
2. **Chunker**: Splits text into 700-1000 character chunks with overlaps, ensuring traceability to the original page.
3. **Structured Extractor**: Uses regex (and optionally LLMs) to extract dates, money, and entities.
4. **Vector Store & Retriever**: Stores chunk embeddings in ChromaDB and allows for hybrid search.
5. **Draft Generator**: Prompts the LLM (or mock) with retrieved evidence and extracted facts.
6. **Edit Learner**: Compares user edits against generated drafts to derive generalizable rules.
