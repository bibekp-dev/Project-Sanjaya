from fastapi import FastAPI
from pydantic import BaseModel
from app.services.vector_store import VectorStore 

app = FastAPI(title="Project Sanjaya API")

# Initialize our Vector Store
db_service = VectorStore() 

class IngestRequest(BaseModel):
    text: str
    filename: str

@app.post("/ingest")
async def ingest_document(payload: IngestRequest):
    metadata = {"source": payload.filename}
    
    # Polymorphism in action: The API doesn't know about chunks, just "upsert"
    success = await db_service.upsert(payload.text, metadata)
    
    return {
        "status": "success", 
        "mode": db_service.__class__.__name__, 
        "message": "Document processed successfully"
    }