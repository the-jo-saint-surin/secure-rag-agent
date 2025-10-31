
import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_texts_from_dir(path: str) -> List[str]:
    texts = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    for root, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if f.lower().endswith(('.txt', '.md')):
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    raw = fh.read()
                for chunk in splitter.split_text(raw):
                    texts.append(chunk)
            elif f.lower().endswith('.pdf'):
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(fp)
                    raw = "\n".join([p.extract_text() or "" for p in reader.pages])
                    for chunk in splitter.split_text(raw):
                        texts.append(chunk)
                except Exception as e:
                    print(f"[warn] Failed to parse PDF {fp}: {e}")
    return texts
