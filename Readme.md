# 📌 Docusights API  
Docusights API is a **document intelligence service** that extracts **text and table data** using **Azure Document Intelligence**, generates **embeddings** with **NVIDIA NV Embed API**, and enables **semantic search** with **FAISS**.

---

## 🚀 Features  
✔ **📄 Document Analysis** → Extracts text, tables, and structure from documents.  
✔ **🔍 Semantic Search** → Uses NVIDIA NV Embed API to generate embeddings and FAISS for fast retrieval.  
✔ **⚡ FastAPI-Based API** → Provides easy-to-use endpoints with **Swagger UI (`/docs`)**.  
✔ **🐳 Docker Support** → Easily deployable with Docker.  

---

## ⚙️ NVIDIA Technologies Used  

### **1️⃣ NVIDIA NV Embed API**  
Docusights uses **NVIDIA's NV Embed API** to generate **high-quality text embeddings** for semantic search.  
🔹 **Model:** `nvidia/nv-embedqa-e5-v5`  
🔹 **Use Case:** Converts text into numerical embeddings to enable similarity-based retrieval.  
🔹 **API Endpoint:** `https://integrate.api.nvidia.com/v1/embeddings`  

### **2️⃣ FAISS (Facebook AI Similarity Search)**  
FAISS is used for **efficient nearest neighbor search** on high-dimensional embeddings.  
🔹 **Why FAISS?** It allows **fast and scalable** document similarity search.  
🔹 **Implementation:** Uses **HNSW (Hierarchical Navigable Small World)** indexing for fast lookup.  

---

## 📂 API Endpoints  

### **1️⃣ Home**  
📌 **`GET /`**  
📌 **Description:** Returns a welcome message.  

### **2️⃣ Analyze Document**  
📌 **`GET /analyze`**  
📌 **Description:**  
- Uses **Azure Document Intelligence** to extract text and tables from documents.  
- Generates **embeddings** for extracted text using NVIDIA API.  
- Stores embeddings in **FAISS** for fast retrieval.  

### **3️⃣ Semantic Search**  
📌 **`POST /query`**  
📌 **Description:**  
- Takes a **query text** and searches similar content using FAISS.  
- Returns **relevant text snippets**.  

📌 **Request Example:**  
```json
{
    "text": "Common stock value per share",
    "k": 5
}

📌 **Request Example:**  
```json
{
    "text": "Common stock value per share",
    "k": 5
}
