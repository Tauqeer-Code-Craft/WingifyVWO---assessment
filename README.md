# Financial Document Analyzer

### CrewAI Debug Challenge Submission

## Overview

This project is a production-oriented **Financial Document Analyzer** built using:

* FastAPI (API layer)
* CrewAI (Agent orchestration)
* Celery + Redis (async job queue)
* SQLite (job tracking persistence)
* Structured prompt engineering
* Deterministic mock execution mode

The assignment focused on:

* Debugging deterministic code failures
* Fixing unsafe / malicious prompt instructions
* Making the system reliable and production-ready
* Ensuring end-to-end execution without real API keys
* Improving architectural quality

---

# Key Improvements Made

This submission does **not** only make the code “run”.
It restructures the system to reflect real-world backend patterns.

Major improvements include:

* Fixed critical deterministic runtime errors
* Removed unsafe prompt behavior (hallucination encouragement)
* Added structured JSON output enforcement
* Implemented async job queue with Celery
* Added persistent job tracking using SQLite
* Introduced mock execution mode for deterministic testing
* Cleaned architecture into modular components
* Improved error handling and lifecycle management

---

# 🏗 System Architecture

### High-Level Flow

```
Client
   ↓
FastAPI (HTTP layer)
   ↓
Redis (Broker)
   ↓
Celery Worker
   ↓
CrewAI Agent
   ↓
PDF Tool
   ↓
SQLite (store result)
```

---

# 📁 Project Structure

```
financial-document-analyzer/
│
├── main.py               # FastAPI application
├── celery_worker.py      # Background worker
├── crew_setup.py         # Crew initialization
├── agents.py             # Agent definitions
├── tasks.py              # Task definitions
├── tools.py              # PDF reader tool
├── database.py           # SQLite ORM models
├── config.py             # Environment configuration
├── requirements.txt
└── README.md
```

---

# Bugs Identified & Fixed

## 1️⃣ Undefined LLM Initialization

Original:

```python
llm = llm
```

Result: Immediate runtime failure.

Fix:
Proper LLM initialization with environment configuration and mock fallback.

---

## 2️⃣ Route Function Name Shadowing

API route function overwrote imported task name.

Impact:
Task object became inaccessible.

Fix:
Renamed API route to avoid namespace collision.

---

## 3️⃣ Missing File Context in Crew Execution

Original code did not pass `file_path` into crew context.

Fix:

```python
crew.kickoff({
    "query": query,
    "file_path": file_path
})
```

---

## 4️⃣ Undefined PDF Loader

Original code used undefined `Pdf()` class.

Fix:
Replaced with `PyPDFLoader` from `langchain-community`.

---

## 5️⃣ Blocking Execution in Async Endpoint

Crew execution blocked FastAPI event loop.

Fix:
Moved execution into Celery background worker.

---

## 6️⃣ Unsafe Prompt Engineering

Original prompt:

* Encouraged hallucination
* Encouraged fake citations
* Encouraged ignoring source document
* Allowed financial advice violations

Fix:
Rewrote prompts to enforce:

* Document-grounded analysis
* Structured JSON output
* Explicit limitation handling
* No fabrication of metrics

---

# Prompt Engineering Improvements

The updated prompt enforces:

* Strict evidence-based reasoning
* Extraction of financial metrics
* Risk identification
* Investment insight (not advice)
* Confidence scoring
* JSON-only output

Expected output format:

```json
{
  "summary": "...",
  "key_metrics": {...},
  "risk_factors": [...],
  "investment_insight": "...",
  "confidence_level": "low/medium/high"
}
```

This ensures deterministic parsing and reliability.

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```
git clone <repository_url>
cd financial-document-analyzer
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

# 🔄 Running the System

## Step 1: Start Redis

If installed locally:

```
redis-server
```

Or with Docker:

```
docker run -p 6379:6379 redis
```

---

## Step 2: Start Celery Worker

```
celery -A celery_worker.celery_app worker --loglevel=info
```

---

## Step 3: Start FastAPI

```
uvicorn main:app --reload --port 8000
```

---

# 🔌 API Documentation

---

## POST `/analyze`

Submits a new financial analysis job.

### Form Data

| Field | Type   | Required |
| ----- | ------ | -------- |
| file  | PDF    | Yes      |
| query | String | Yes      |

### Response

```
{
  "status": "submitted",
  "job_id": "<uuid>"
}
```

---

## GET `/result/{job_id}`

Fetch job status and result.

### Possible Responses

```
{
  "status": "pending"
}
```

```
{
  "status": "processing"
}
```

```
{
  "status": "completed",
  "result": "{...json...}"
}
```

```
{
  "status": "failed",
  "result": "error message"
}
```

---

# 🗄 Database Design

Table: `analysis_jobs`

| Field      | Description                               |
| ---------- | ----------------------------------------- |
| id         | Unique job ID                             |
| filename   | Uploaded file name                        |
| query      | User query                                |
| status     | pending / processing / completed / failed |
| result     | JSON result                               |
| created_at | Timestamp                                 |

---

# Mock Mode (No API Key Required)

Since API keys were not provided in the assignment, a deterministic mock mode was implemented.

Default behavior:

```
USE_MOCK=true
```

This ensures:

* Reproducible execution
* No external dependency
* Evaluator-friendly setup

To enable real LLM execution:

```
USE_MOCK=false
OPENAI_API_KEY=<your_key>
```

---

# Production Considerations

The system is designed to reflect real-world patterns:

* Async job execution (Celery)
* Persistent storage
* Separation of concerns
* Tool-based document ingestion
* Structured LLM outputs
* Deterministic fallback mode

---

# Future Improvements

* Add RAG for large financial reports
* Implement chunked PDF processing
* Add financial ratio computation engine
* Add automated test suite (pytest)
* Add request rate limiting
* Add structured logging & monitoring
* Add Docker Compose for full stack

---

# Testing Approach

Current validation includes:

* Mock-mode deterministic runs
* Manual API testing via Swagger UI
* Job lifecycle validation
* JSON schema validation

---

# Design Decisions

| Decision               | Reason                               |
| ---------------------- | ------------------------------------ |
| Celery integration     | Prevent API blocking                 |
| SQLite                 | Lightweight persistence              |
| Mock mode              | Deterministic execution without keys |
| Structured JSON output | Safe parsing                         |
| Separate modules       | Maintainability                      |

---

# 🏁 Conclusion

This project was transformed from a partially broken prototype into a:

* Deterministic
* Structured
* Safe
* Asynchronous
* Production-ready
* Extensible GenAI system

The focus was not only on making it work, but on making it reliable and scalable.

---
