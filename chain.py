
import os
from typing import Dict, Any, List
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from .utils.vectorstore import get_vectorstore

def build_chain() -> RetrievalQA:
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        temperature=0.2,
    )
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )
    return chain

def format_sources(docs: List[Any]) -> List[Dict[str, str]]:
    out = []
    for d in docs or []:
        meta = d.metadata or {}
        out.append({
            "source": meta.get("source", "unknown"),
            "preview": (d.page_content or "")[:200]
        })
    return out
