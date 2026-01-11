# 🧘 Ask Me Anything About Yoga (RAG Micro-App)

A full-stack AI micro-product that answers yoga & fitness related queries using a RAG pipeline with built-in safety guardrails and MongoDB logging.

## 🚀 Project Overview
This application allows users to ask questions about Yoga poses, benefits, and contraindications. It uses a **Hybrid RAG approach**:
- **Vector Search:** FAISS (Local) with HuggingFace embeddings.
- **LLM:** Google Gemini 1.5 Flash.
- **Safety:** Hard-coded logic to flag high-risk medical queries (e.g., pregnancy, glaucoma).
- **Logging:** All interactions are stored in MongoDB Atlas for analysis.

## 📂 Repository Structure
- `/frontend`: Streamlit UI logic.
- `/backend`: Core RAG pipeline, Safety logic, and Database connection.
- `/data`: The knowledge base text file.

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone <your-repo-link>
cd yoga-rag-app

pip install -r requirements.txt


streamlit run frontend/app.py


You will need to input these in the App Sidebar:
Gemini API Key: For generating answers.
MongoDB URI: For logging data.





Technical Implementation
1. RAG Pipeline
Chunking: We use RecursiveCharacterTextSplitter (500 tokens). This size was chosen to keep yoga instructions complete without losing context.
Embeddings: all-MiniLM-L6-v2. A lightweight, local model chosen for speed and privacy.
Vector DB: FAISS (CPU). Chosen for zero-latency retrieval without needing external API calls for storage.
2. Safety Logic (backend/safety.py)
A check_safety(query) function intercepts the user input before it reaches the LLM.
It scans for keywords: pregnant, hernia, glaucoma, surgery, etc.
If found, it returns is_unsafe = True and displays a Red Warning Block instead of an AI answer.
This prevents the AI from giving medical advice on risky conditions.
3. Data Models (MongoDB)
We store logs in the interaction_logs collection with this schema:

{
  "timestamp": "2026-01-11T10:00:00Z",
  "user_query": "Is headstand safe for glaucoma?",
  "ai_response": "⚠️ SAFETY ALERT...",
  "is_unsafe": true,
  "retrieved_chunks": []
}



Mobile App (.apk)
This application is designed as a Responsive Web App. To test it on mobile:
Open the hosted Streamlit URL on a mobile browser.
It adapts perfectly to small screens.
(Note: A native .apk was not generated as the core logic relies on Python runtime, which is best served via Web)


