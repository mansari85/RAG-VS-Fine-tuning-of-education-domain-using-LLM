# RAG vs Fine-Tuning: Educational Domain LLM Evaluation Platform

> **Academic Research Project:** *"RAG vs Fine-Tuning for Domain-Specific Large Language Models"*  
> **Domain:** Educational Materials (Chemistry, Physics, Data Structures, Data Communication, Economics, University Policies)  
> **Target Environment:** 100% Local, CPU-Compatible, Zero Paid APIs, 16 GB RAM

---

## 1. Project Structure

```
RAG-VS-FINE-TUNING/
│
├── backend/                       # FastAPI application & server routes
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # Backend configuration
│   │   └── routes/
│   │       ├── ai.py              # POST /api/rag/query endpoint
│   │       ├── knowledge_base.py  # Knowledge base inspection endpoints
│   │       └── ...
│   ├── requirements.txt           # Backend python dependencies
│   └── .env                       # Environment variables
│
├── frontend/                      # React + Vite + Tailwind educational web interface
│   ├── src/
│   │   ├── pages/                 # AskQuestionPage.jsx (Educational Chatbot interface)
│   │   └── services/              # API client and endpoints.js
│   └── package.json
│
├── RAG/                           # RAG SYSTEM IMPLEMENTATION (Isolated & Model-Agnostic)
│   ├── config.py                  # Centralized RAG configuration
│   ├── index_cli.py               # CLI utility to build/rebuild FAISS index
│   ├── pipeline.py                # 7-step RAG pipeline orchestrator
│   ├── ingestion/                 # Document ingestion modules
│   │   ├── pdf_loader.py          # Page-by-page PDF extraction
│   │   ├── pptx_loader.py         # Slide-by-slide PPTX extraction
│   │   ├── docx_loader.py         # Paragraph & table DOCX extraction
│   │   └── ingest.py              # Recursive scanner & category mapper
│   ├── processing/                # Text processing
│   │   ├── cleaner.py             # Artifact, spacing, and hyphenation cleaner
│   │   └── chunker.py             # Configurable recursive chunker preserving metadata
│   ├── embeddings/                # Embedding generation
│   │   └── embedder.py            # Sentence-transformers on CPU
│   ├── vector_store/              # FAISS Vector Database
│   │   ├── vector_store.py        # FAISS IndexFlatIP & metadata mapping
│   │   ├── index.faiss            # Persisted vector index
│   │   └── metadata.json          # Chunk metadata mapping
│   ├── models/                    # Model loading layer (Model-Agnostic)
│   │   └── model_loader.py        # Lazy loading of local Hugging Face LLM on CPU
│   ├── generation/                # RAG Generation layer
│   │   └── rag_generator.py       # Factual, grounded context & prompt generator
│   └── tests/                     # Verification & benchmark test suite
│       ├── test_rag_system.py     # 13 automated tests across full pipeline
│       └── validate_rag.py        # Academic domain validation across subjects
│
├── Datasets/                      # ORIGINAL DATASET (Preserved & Unmodified)
│   └── RAG/                       # 45 educational course documents
│       ├── Chemistry PDF/
│       ├── Data communication and Networks/
│       ├── data structure and algorithms/
│       ├── Economic/
│       ├── Physics/
│       └── University Policies & Handbooks (.pdf)
│
├── Fine-Tuning/                   # Reserved for future fine-tuning phase
├── Hybrid/                        # Reserved for future hybrid phase
├── models/                        # Local model weights / Hugging Face cache
├── requirements.txt               # CPU-compatible package manifest
└── start-platform.cmd             # Quick launcher for Windows
```

---

## 2. Hardware Constraints & Requirements

- **Processor:** Any modern multi-core x86_64 CPU (Intel / AMD).
- **RAM:** Minimum 8 GB (16 GB recommended).
- **GPU:** **No NVIDIA GPU required.** Runs strictly on CPU with Intel integrated graphics.
- **CUDA:** Not required. PyTorch runs in pure CPU mode (`device="cpu"`).
- **Storage:** ~5 GB free space for model weights and cache.

---

## 3. Default Local Models

| Component | Default Model | Type | Memory / Dim |
|---|---|---|---|
| **Local LLM** | `Qwen/Qwen2.5-1.5B-Instruct` | Local Hugging Face | ~3.0 GB RAM |
| **Embedding** | `sentence-transformers/all-MiniLM-L6-v2` | SentenceTransformers | 384 dimensions |
| **Vector DB** | `FAISS CPU` (`IndexFlatIP`) | In-memory + Disk | Cosine similarity |

> **Zero Paid APIs:** Completely local and free of OpenAI, Gemini, Anthropic, or external API keys.

---

## 4. Installation

Ensure you have **Python 3.10 - 3.12** installed on Windows.

### 4.1. Setup Python Virtual Environment

```powershell
# From project root:
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r ..\requirements.txt
cd ..
```

### 4.2. Setup Frontend

```powershell
cd frontend
npm install
cd ..
```

---

## 5. Dataset Location

The educational materials remain in `Datasets/` without alteration:
```
Datasets/RAG/
  ├── Chemistry PDF/
  ├── Data communication and Networks/
  ├── data structure and algorithms/
  ├── Economic/
  ├── Physics/
  └── [University Policy & Curriculum PDFs]
```
The ingestion layer discovers all `.pdf`, `.pptx`, and `.docx` files recursively and maps them to academic categories.

---

## 6. How to Build the FAISS Vector Index

A dedicated CLI script builds the index independently. The FastAPI server does **not** rebuild the index on restart.

```powershell
# Activate backend environment
.\backend\.venv\Scripts\activate

# Run standalone indexing
python -m RAG.index_cli --rebuild
```

**Custom options:**
```powershell
python -m RAG.index_cli --rebuild --chunk-size 500 --chunk-overlap 50
```

This generates:
- `RAG/vector_store/index.faiss` (FAISS CPU IndexFlatIP with 2,805 vectors)
- `RAG/vector_store/metadata.json` (Provenance mapping for each chunk)
- `RAG/vector_store/processed_documents.json` (Extracted document units)

---

## 7. How to Start FastAPI Backend

```powershell
# Terminal 1:
cd backend
.\.venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive API documentation will be available at:
- **Swagger Docs:** `http://localhost:8000/api/docs`
- **ReDoc:** `http://localhost:8000/api/redoc`

---

## 8. How to Start the Frontend

```powershell
# Terminal 2:
cd frontend
npm run dev
```

Open your browser at **`http://localhost:5173`**.  
Navigate to the **Ask a Question** page to interact with the local RAG system.

---

## 9. How to Test the API

### Via cURL (PowerShell / Command Prompt):
```powershell
curl -X POST "http://localhost:8000/api/rag/query" `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What is the attendance requirement for engineering students?\"}'
```

### Expected JSON Response:
```json
{
  "answer": "To be eligible for examinations and placements, students must maintain a minimum attendance of 75% across courses (80% for placement training)...",
  "sources": [
    {
      "file": "University_Policies_Discipline_Security_Attendance.pdf",
      "page": 1,
      "score": 0.6936
    }
  ],
  "question": "What is the attendance requirement for engineering students?",
  "model_used": "Qwen/Qwen2.5-1.5B-Instruct",
  "response_time_ms": 31800,
  "token_count": 80,
  "approach": "RAG"
}
```

---

## 10. How to Run the Automated Test Suite

### Full 13-Part Unit & Integration Test Suite:
```powershell
python RAG/tests/test_rag_system.py
```
This tests:
1. Dataset discovery
2. PDF extraction (page-by-page)
3. PPTX extraction (slide-by-slide)
4. DOCX extraction (paragraphs & tables)
5. Text cleaning (whitespace, hyphenation)
6. Semantic chunking & metadata preservation
7. Sentence-transformers embedding generation on CPU
8. FAISS vector indexing & verification
9. Semantic similarity retrieval
10. Local LLM lazy loading on CPU
11. Grounded RAG answer generation
12. Complete end-to-end pipeline execution
13. FastAPI `POST /api/rag/query` HTTP endpoint

### Academic Domain Validation Benchmark:
```powershell
python RAG/tests/validate_rag.py
```
Tests queries in Chemistry, Physics, Data Structures, Data Communication, Economics, University Policies, and Out-of-Domain anti-hallucination.

---

## 11. Model-Agnostic Design: Changing the Models

### Changing the LLM:
You can switch the LLM to any Hugging Face causal LM compatible with your CPU/RAM via environment variable:
```bash
# In backend/.env or RAG/config.py
LLM_MODEL=meta-llama/Llama-3.2-1B-Instruct
# or
LLM_MODEL=microsoft/Phi-3-mini-4k-instruct
```
> **CRITICAL:** Changing the LLM **does NOT** require rebuilding the FAISS index because the document embeddings have not changed.

### Changing the Embedding Model:
```bash
# In backend/.env or RAG/config.py
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```
> **IMPORTANT:** Changing the embedding model changes vector dimensionality and embedding representations. **You MUST rebuild the FAISS index:**
> ```powershell
> python -m RAG.index_cli --rebuild
> ```

---

## 12. Troubleshooting & FAQ

1. **Slow generation on CPU?**
   - The default model is `Qwen/Qwen2.5-1.5B-Instruct`, which runs in ~15-30 seconds on modern quad-core/hexa-core CPUs.
   - For even faster generation, you can lower `MAX_NEW_TOKENS=128` in `.env`.
   - Never use 7B or 13B models on CPU without GPU acceleration.

2. **Index missing error (`HTTP 503: FAISS vector index is not built`)?**
   - Run `python -m RAG.index_cli --rebuild` to create `index.faiss` and `metadata.json`.

3. **OutOfMemory (OOM) during embedding generation?**
   - Lower the batch size: `EMBEDDING_BATCH_SIZE=16` in `RAG/config.py`.
