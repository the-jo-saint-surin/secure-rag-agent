
import os
from typing import Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def get_vectorstore(persist_dir: Optional[str] = None):
    persist_dir = persist_dir or os.getenv("CHROMA_DIR", "chroma")
    os.makedirs(persist_dir, exist_ok=True)
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"))
    vs = Chroma(embedding_function=embeddings, persist_directory=persist_dir)
    return vs
