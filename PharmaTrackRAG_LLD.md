# PharmaTrackRAG - Low Level Design (LLD)

## 1. Architecture Overview
- **Ingestion Service**: Handles document upload, parsing, chunking, embeddings, and indexing.
- **Vector Store**: FAISS index + SQLite metadata database.
- **Retrieval API**: FastAPI service for semantic search and RAG-based answering.
- **Generation Module**: Local/HuggingFace model synthesizing answers from retrieved context.
- **UI Layer**: Gradio or React frontend.

## 2. Data Models

### Document
- `document_id` (UUID)  
- filename  
- metadata  
- uploaded_at  
- status  

### Chunk
- `chunk_id` (UUID)  
- `document_id`  
- text  
- embedding_id  
- start_offset / end_offset  
- created_at  

## 3. Algorithms

### Chunking
- ~500 token chunks  
- 50 token overlap  
- Sentence-aware splitting  

### Embeddings
- Model: `sentence-transformers/all-MiniLM-L6-v2`  
- 384-dim vectors  
- L2-normalized  

### Retrieval
- FAISS `IndexFlatIP`  
- Top-k search (default: 8)  
- Similarity threshold: 0.65 for confidence  

## 4. API Endpoints

### POST `/documents/upload`
Upload document for parsing/indexing.

### POST `/documents/{id}/index`
Triggers ingestion + embedding + FAISS indexing.

### POST `/search`
Semantic search returning top-k relevant chunks.

### POST `/answer`
RAG pipeline → retrieved chunks → LLM synthesis → citations.

## 5. Prompt Structure

### System Prompt
- Evidence-grounded responses only  
- Mandatory citations  
- No unsupported claims  

### User Prompt
- Injected context chunks  
- Query  
- Output rules (citations, confidence, fallback behavior)

## 6. Guardrails
- Evidence thresholding  
- Citation validation  
- Low-confidence fallback  
- PII redaction during ingestion  

## 7. Deployment
- Dockerized FastAPI services  
- HF Spaces or local hosting for UI  
- Persistent storage for FAISS + SQLite  

## 8. Monitoring
- Log retrieval scores  
- Latency metrics  
- Prometheus-compatible `/metrics` endpoint  

## 9. Testing
- Unit tests: parser, chunker, embeddings  
- Integration tests: upload → index → search → answer  
- Snapshot tests for prompt outputs  

## 10. Implementation Phases

### Phase A – Core Pipeline
- Ingestion  
- Chunking  
- Embeddings  
- FAISS search  

### Phase B – RAG Answering
- LLM generation  
- Guardrails + citation validator  

### Phase C – Monitoring
- Logging, metrics, evaluation harness  

### Phase D – Enhancements
- Re-ranking  
- UI improvements  
- API auth  
