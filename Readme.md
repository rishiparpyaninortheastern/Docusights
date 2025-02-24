# 📌 Docusights API  
Docusights API is a **document intelligence service** that extracts **text and table data** using **Azure Document Intelligence**, generates **embeddings** with **NVIDIA NV Embed API**, and enables **semantic search** with **FAISS**.

---

## 🚀 Features  
✔ **📄 Document Analysis** → Extracts text, tables, and structure from documents.  
✔ **🔍 Semantic Search** → Uses NVIDIA NV Embed API to generate embeddings and FAISS for fast retrieval.  
✔ **⚡ FastAPI-Based API** → Provides easy-to-use endpoints with **Swagger UI (`/docs`)**.  
✔ **🐳 Docker Support** → Easily deployable with Docker.  

---

## 📂 API Endpoints  

### **1️⃣ Home**  
📌 **`GET /`**  
📌 **Description:** Returns a welcome message.  

### **2️⃣ Analyze Document**  
📌 **`GET /analyze`**  
📌 **Description:**  
- Uses **Azure Document Intelligence** to extract text and tables from documents.  
- Generates **embeddings** for extracted text.  
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
