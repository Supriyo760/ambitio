# Assumptions and Tradeoffs

1. **Mock LLM by Default**: Given API key constraints for reviewers, the system defaults to a Mock LLM that simulates an 8-section output. Hooking up a real OpenAI API simply requires switching the adapter.
2. **SQLite and Local ChromaDB**: Chosen for ease of local setup by reviewers over PostgreSQL/pgvector.
3. **OCR Tooling**: Used PyTesseract. In a production legal tech environment, cloud APIs (like AWS Textract or GCP Document AI) would provide significantly better accuracy on messy, handwritten, or skewed documents.
4. **Edit Learning**: We use a transparent prompt-based rule extraction mechanism rather than fine-tuning a model on edits. This is more practical for an MVP and provides explicit, reviewable rules.
