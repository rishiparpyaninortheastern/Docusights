import json
import numpy as np
import faiss
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
from fastapi import Query
app = FastAPI()
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

# Azure Document Intelligence credentials
endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

# NVIDIA API credentials
API_KEY = os.getenv("NVIDIA_API_KEY")
url = os.getenv("NVIDIA_API_URL")

# FAISS index and storage
index = None
all_data = {}
d = None

class QueryRequest(BaseModel):
    text: str
    k: int = 5

def get_embedding(text):
    """Get embedding from NVIDIA API"""
    payload = {
        "model": "nvidia/nv-embedqa-e5-v5",
        "encoding_format": "float",
        "truncate": "NONE",
        "input_type": "passage",
        "input": text
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    embedding_data = response.json()
    
    if embedding_data["object"] == "list" and embedding_data["data"]:
        embedding_list = embedding_data["data"][0]["embedding"]
        embedding_np = np.array(embedding_list, dtype=np.float32)
        return embedding_np / np.linalg.norm(embedding_np)
    return None

def build_faiss_index(embeddings):
    """Build FAISS index for search"""
    global d, index
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

def search_faiss_index(query_embedding, k=5):
    """Search FAISS index"""
    if index is None:
        return []
    query_embedding = query_embedding.reshape(1, -1)
    D, I = index.search(query_embedding, k)
    return I[0].tolist()

@app.get("/")
def home():
    return {"message": "Welcome to the Document Intelligence API"}

@app.get("/analyze")
def analyze_layout(document_url: str = Query(..., description="URL of the document to analyze")):
    """Extract text and embeddings from a document"""
    global all_data
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    poller = client.begin_analyze_document("prebuilt-layout", AnalyzeDocumentRequest(url_source=document_url))
    result: AnalyzeResult = poller.result()

    all_data["pages"] = []
    embeddings_list = []

    for page in result.pages:
        page_info = {"page_number": page.page_number, "lines": []}
        all_data["pages"].append(page_info)

        if page.lines:
            for line in page.lines:
                embedding = get_embedding(line.content)
                if embedding is not None:
                    embeddings_list.append(embedding)
                page_info["lines"].append({"text": line.content, "embedding": embedding.tolist() if embedding is not None else None})

    if embeddings_list:
        embeddings_array = np.array(embeddings_list).astype('float32')
        build_faiss_index(embeddings_array)

    return all_data
@app.get("/query")
def query_data(query: QueryRequest = Query(...)):
    """Search for relevant text using FAISS"""
    query_embedding = get_embedding(query.text)
    if query_embedding is None:
        return {"error": "Failed to generate embedding"}
    
    indices = search_faiss_index(query_embedding, query.k)
    results = []
    
    for idx in indices:
        for page in all_data["pages"]:
            for line in page["lines"]:
                if "embedding" in line and line["embedding"] is not None:
                    if np.array_equal(np.array(line["embedding"]), index.reconstruct(idx)):
                        results.append(line["text"])
                        if len(results) >= query.k:
                            break
            if len(results) >= query.k:
                break
        if len(results) >= query.k:
            break

    return {"query": query.text, "matches": results}


if __name__ == "__main__":
  

    uvicorn.run(app, host="0.0.0.0", port=8000)
