from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from . import models
from .db import engine
from .routers import matters, documents, extraction, retrieval, drafts, learning, evaluation

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grounded Legal Drafting Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matters.router)
app.include_router(documents.router)
app.include_router(extraction.router)
app.include_router(retrieval.router)
app.include_router(drafts.router)
app.include_router(learning.router)
app.include_router(evaluation.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "llm_provider": "mock",
        "vector_store": "ready"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
