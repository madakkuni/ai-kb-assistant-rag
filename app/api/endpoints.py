import os
import time
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from app.langgraph.workflow import rag_workflow
from app.langgraph import nodes
from app.langgraph.nodes import init_components
from app.ingestion.document_loader import DocumentIngestor
from app.services.tracking import MetricsTracker

router = APIRouter()
tracker = MetricsTracker()
ingestor = DocumentIngestor()

class ChatRequest(BaseModel):
    query: str
    
@router.on_event("startup")
async def startup_event():
    init_components()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not nodes.retriever_instance:
        # Retry init
        init_components()
        if not nodes.retriever_instance:
            raise HTTPException(status_code=500, detail="Retriever not initialized")
        
    os.makedirs("data/documents", exist_ok=True)
    file_location = f"data/documents/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
        
    try:
        docs = await ingestor.ingest_file(file_location, file.filename)
        nodes.retriever_instance.add_documents(docs)
        return {"filename": file.filename, "status": "Ingested", "chunks": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest-all")
async def ingest_all_documents():
    if not nodes.retriever_instance:
        init_components()
        if not nodes.retriever_instance:
            raise HTTPException(status_code=500, detail="Retriever not initialized")
            
    docs_dir = "data/documents"
    if not os.path.exists(docs_dir):
        return {"status": "No documents directory found", "processed": 0}
        
    supported_extensions = {".pdf", ".docx", ".txt", ".md"}
    results = {"processed": 0, "failed": 0, "total_chunks": 0, "errors": []}
    
    for filename in os.listdir(docs_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in supported_extensions:
            file_path = os.path.join(docs_dir, filename)
            try:
                docs = await ingestor.ingest_file(file_path, filename)
                nodes.retriever_instance.add_documents(docs)
                results["processed"] += 1
                results["total_chunks"] += len(docs)
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({"filename": filename, "error": str(e)})
                
    return results

@router.post("/chat")
async def chat(request: ChatRequest, eval: bool = Query(False)):
    try:
        start_time = time.time()
        
        initial_state = {
            "query": request.query,
            "top_k": int(os.environ.get("TOP_K", 5)),
            "rerank_top_k": int(os.environ.get("RERANK_TOP_K", 3)),
            "eval_mode": eval
        }
        
        final_state = rag_workflow.invoke(initial_state)
        
        latency = time.time() - start_time
        
        tracker.track_request(
            query=request.query,
            latency=latency,
            token_usage=final_state.get("token_usage", {})
        )
        
        return {
            "answer": final_state.get("answer"),
            "sources": final_state.get("sources", []),
            "evaluation": final_state.get("evaluation_metrics"),
            "metrics": {
                "latency_sec": round(latency, 2),
                "tokens": final_state.get("token_usage", {})
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to process request. Please try again. ({str(e)})")

@router.get("/metrics")
async def get_metrics():
    return tracker.get_aggregate_metrics()

@router.get("/history")
async def get_history():
    data = tracker._read_metrics()
    return {"history": data.get("requests", [])[-50:]}
