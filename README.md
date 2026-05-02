# WikiRAG

A Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **Qdrant**, and a local LLM (via Ollama).
Supports **text** and optional **voice (TTS)** responses, basic **guardrails**, and **session-based conversations**.

---

## Features

*  Vector search with Qdrant
*  LLM-based answer generation (Gemma via Ollama)
*  Reranking with cross-encoder
*  Guardrails (basic + LLM-based)
*  Session handling
*  Optional voice output (TTS)
*  Docker support (Qdrant, Redis)

---

## Tech Stack

* Python 3.11
* FastAPI
* Qdrant (vector DB)
* Redis (cache / future use)
* SentenceTransformers (embeddings)
* Cross-encoder reranker (local clone)
* Ollama (LLM)
* pyttsx3 (TTS, optional)

---

## Setup

### 1. Clone repository

```bash
git clone <your-repo-url>
cd WikiRAG
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run infrastructure (Docker)

```bash
docker compose up -d
```

This starts:

* Qdrant → `http://localhost:6333`
* Redis → `localhost:6379`

---

### 5. Install Ollama & pull model

Install Ollama manually:
https://ollama.com/

Then:

```bash
ollama pull gemma:2b
```

---

### 6. Reranker setup (IMPORTANT)

The reranker **must be cloned locally**:

```bash
git clone https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2
```

Then update your config to point to the local path:

```text
C:\path\to\ms-marco-MiniLM-L-6-v2
```

---

### 7. Configure project

Edit your config file (e.g. `config.cfg` or `.env`):

```ini
[LLM]
model_name = gemma:2b
url = http://localhost:11434/api/generate

[RERANKER]
path = C:\path\to\ms-marco-MiniLM-L-6-v2
```

---

### 8. Run backend

```bash
uvicorn app.api:app --reload
```

---

## API Usage

### Health check

```bash
GET /health
```

---

### Chat (text)

```python
import requests

res = requests.post(
    "http://localhost:8000/chat",
    json={"query": "Who invented the light bulb?"}
)

print(res.json())
```

---

### Chat (audio)

```python
import requests

res = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "Who invented the light bulb?",
        "response_format": "audio"
    }
)

with open("answer.wav", "wb") as f:
    f.write(res.content)
```

---

## Notes & Limitations

* ⚠️ Designed primarily for **Windows** (TTS uses system voices)
* ⚠️ Reranker must be **downloaded manually**
* ⚠️ Ollama must be installed separately
* ⚠️ TTS is **blocking** and not optimized for high concurrency yet
* ⚠️ Sessions are currently **in-memory**

---

## Project Structure

```text
core/           # config, logging, embeddings, auth (future)
services/       # pipeline, guardrails, TTS
models/         # Pydantic schemas
app/            # FastAPI app
```

---

## Development Notes

* Use `uvicorn --reload` for development
* Logging is configured per-module
* Guardrails are extensible (LLM + rule-based)
* CI uses Ruff + MyPy (can be disabled)

---

## Roadmap

* [ ] Async pipeline
* [ ] Redis-backed sessions
* [ ] Streaming responses
* [ ] Improved guardrails
* [ ] Better TTS engine (async / neural)
* [ ] Authentication & user management

---

## License

MIT (or your choice)
