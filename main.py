
import os
from typing import Optional
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .security import verify_api_key
from .chain import build_chain, format_sources
from .utils.loader import load_texts_from_dir
from .utils.vectorstore import get_vectorstore

load_dotenv()

app = FastAPI(title="Secure RAG Agent", version="0.1.0")

class IngestRequest(BaseModel):
    path: str = Field(..., description="Directory path containing txt/md/pdf files")

class AskRequest(BaseModel):
    query: str = Field(..., description="Natural language question to ask the agent")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(req: IngestRequest, ok: bool = Depends(verify_api_key)):
    texts = load_texts_from_dir(req.path)
    if not texts:
        return {"ingested": 0, "message": "No parsable documents found."}
    vs = get_vectorstore()
    vs.add_texts(texts=texts, metadatas=[{"source": req.path}] * len(texts))
    vs.persist()
    return {"ingested": len(texts), "message": f"Ingested from {req.path}"}

@app.post("/ask")
def ask(req: AskRequest, ok: bool = Depends(verify_api_key)):
    chain = build_chain()
    res = chain({"query": req.query})
    answer = res.get("result", "").strip()
    sources = format_sources(res.get("source_documents"))
    return {"answer": answer, "sources": sources}
