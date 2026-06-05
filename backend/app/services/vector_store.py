import chromadb
from chromadb.config import Settings
import os

VECTOR_DB_DIR = "chroma_db"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# Persistent ChromaDB client
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

def get_collection(matter_id: str):
    collection_name = f"matter_{matter_id.replace('-', '_')}_chunks"
    return client.get_or_create_collection(name=collection_name)

def add_chunks_to_vector_store(matter_id: str, chunks_data: list[dict]):
    collection = get_collection(matter_id)
    
    ids = []
    documents = []
    metadatas = []
    
    for c in chunks_data:
        ids.append(c["chunk_id"])
        documents.append(c["text"])
        metadatas.append({
            "document_id": c["document_id"],
            "page_number": c["page_number"],
            "confidence": c["confidence"]
        })
        
    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

def semantic_search(matter_id: str, query: str, n_results: int = 5):
    collection = get_collection(matter_id)
    # If collection is empty, this will raise or return empty
    if collection.count() == 0:
        return []
        
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    retrieved = []
    if results['ids'] and len(results['ids']) > 0:
        for i in range(len(results['ids'][0])):
            retrieved.append({
                "chunk_id": results['ids'][0][i],
                "text": results['documents'][0][i],
                "score": 1.0 - (results['distances'][0][i] if 'distances' in results and results['distances'] else 0.0), # Simplistic score inversion
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
            })
    return retrieved
