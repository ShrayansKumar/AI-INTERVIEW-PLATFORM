# AI Interview Platform

An agentic, voice-driven mock interview platform that parses a candidate's resume, retrieves company-specific interview context via RAG, conducts a full voice interview using a 6-agent LangGraph pipeline, and produces a scored report with a downloadable PDF.

Built as a placement portfolio project demonstrating full-stack engineering, multi-agent LLM orchestration, RAG, and voice AI integration.

---

## Features

- **Resume parsing** — PDF upload → text extraction → LLM-based structuring into skills, projects, experience, education, coursework, and extracurriculars
- **Resume RAG** — the full resume is chunked (by section) and embedded, so question generation retrieves and grounds questions in actual resume detail rather than a generic summary
- **Company-specific knowledge base** — 9 companies (Amazon, Google, Microsoft, Meta, Goldman Sachs, Uber, Salesforce, Atlassian, Flipkart) seeded with real interview experiences, OA-style questions, and job description context, retrieved via pgvector similarity search
- **6-agent LangGraph pipeline** — Resume Agent → Question Agent → Interview Agent (with bounded follow-up logic) → Evaluation Agent → Feedback Agent → Report Agent
- **Voice interview loop** — speech-to-text (Groq Whisper), text-to-speech (Groq Orpheus TTS), full record → transcribe → respond → speak round trip
- **Scored reports** — per-question evaluation across technical accuracy, communication, problem solving, and depth, plus an overall recommendation
- **PDF report generation** and downloadable reports
- **Analytics dashboard** — score trend and topic breakdown charts across all completed sessions
- **Admin panel** — separate, independently-authenticated admin system for managing companies, knowledge base entries, and viewing registered users
- **Resume persistence** — uploaded once, reused across future interviews without re-uploading

---

## Tech Stack

**Backend**
- FastAPI + SQLAlchemy (async) + Alembic
- PostgreSQL (Neon) with `pgvector` for embeddings
- Redis (Upstash) + Celery for background tasks
- LangGraph + LangChain for agent orchestration
- Groq (LLM inference, Whisper STT, Orpheus TTS)
- Sentence Transformers (local embeddings, no external embedding API)
- Cloudinary (file storage)
- ReportLab (PDF generation)

**Frontend**
- React + Vite
- Tailwind CSS v4 (custom dark theme — true black background, dark gray cards, teal accent)
- React Router
- Zustand (state management)
- Recharts (analytics charts)
- Axios with automatic token refresh

---

## Architecture Overview

### The 6-Agent Pipeline

```
Resume Agent       → Structures raw resume text into skills/projects/experience/education/coursework/extracurriculars
Question Agent     → Retrieves company knowledge base + ALL resume chunks, generates 5 grounded questions
Interview Agent     → Manages the conversation loop; decides whether an answer needs a follow-up (capped at 1 per question)
Evaluation Agent   → Scores each answer 0-10 on technical accuracy, communication, problem solving, depth
Feedback Agent     → Synthesizes strengths, weaknesses, and improvement areas from the evaluations
Report Agent       → Compiles the final report: averaged metrics, overall score, hire recommendation
```

State flows through all 6 agents via a single `InterviewState` object, persisted to PostgreSQL as JSONB between API calls so a session survives across multiple requests.

### Resume RAG

The full resume — not just a summary — is split into section-based chunks (one per project, the experience section, education, coursework, each extracurricular) using an LLM-based chunker that preserves all bullet-point detail. These chunks are embedded and stored per-user. When generating interview questions, **all** of a user's resume chunks are retrieved (similarity-based filtering was deliberately removed — with only ~10-15 chunks per resume, filtering risked silently dropping relevant sections written in different vocabulary than the retrieval query, e.g. a research-experience chunk full of technical jargon scoring lower than project chunks for a generic query).

### Company Knowledge Base

Each of the 9 seeded companies has ~6 knowledge chunks: a job description, 2 interview experiences, 2 OA-style questions, and 1 topic-focus chunk, all embedded with Sentence Transformers (`all-mpnet-base-v2`, 768-dim) and retrieved via pgvector cosine similarity.

### Voice Loop

```
Browser mic (MediaRecorder) → audio blob → POST /answer-voice
  → Groq Whisper transcribes → text fed into Interview Agent
  → next question generated → Groq Orpheus TTS → base64 audio → browser plays it
```

---

## Project Structure

```
ai-interview-platform/
├── backend/
│   ├── app/
│   │   ├── agents/          # 6 LangGraph agents + state + graph builder
│   │   ├── api/v1/          # Route handlers (auth, admin, admin_auth, resume, interview, voice, report, analytics, company)
│   │   ├── core/            # Security, JWT handling (separate for users and admins)
│   │   ├── db/               # SQLAlchemy session + base
│   │   ├── models/           # ORM models
│   │   ├── schemas/          # Pydantic request/response models
│   │   ├── services/         # Business logic (resume parsing, chunking, retrieval, embeddings, sessions, PDF, analytics)
│   │   ├── tasks/             # Celery app + background tasks
│   │   └── utils/             # File storage, prompt templates
│   ├── alembic/               # Migrations
│   └── scripts/               # Knowledge base seeding
└── frontend/
    └── src/
        ├── components/       # auth/, dashboard/, interview/, resume/, report/, admin/
        ├── routes/            # Page-level components, including admin/ subroutes
        ├── store/             # Zustand stores (auth, admin auth, interview, UI)
        ├── hooks/             # useAudioRecorder, useInterviewSession, useReportData
        └── lib/                # apiClient (user), adminApiClient (admin) — separate token namespaces
```

---

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

Create `backend/.env`:
```
DATABASE_URL=postgresql+asyncpg://...
SQLALCHEMY_DATABASE_URL=postgresql://...
REDIS_URL=rediss://...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
GROQ_API_KEY=...
SECRET_KEY=...
```

Run migrations and seed the knowledge base:
```bash
alembic upgrade head
python scripts/seed_knowledge_base.py
python create_admin.py   # creates the first admin account
```

Start the server:
```bash
uvicorn app.main:app --reload
```

Start the Celery worker (separate terminal, required for background tasks):
```bash
celery -A app.tasks.celery_app worker --loglevel=info --pool=solo
```

### Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:
```
VITE_API_BASE_URL=http://localhost:8000
```

```bash
npm run dev
```

---

## Authentication Model

Two **completely separate** auth systems, intentionally not sharing any code path:

- **Users** — register/login via email, JWT access + refresh tokens, persisted in `localStorage`, auto-refreshed silently
- **Admins** — separate `admins` table, separate JWT signing namespace (`type: admin_access`, rejected by user-facing routes and vice versa), stored in `sessionStorage` (cleared on tab close), no public registration — created via `create_admin.py`

This separation means a regular user's token can never be used against admin routes, even if intercepted.

---

## Known Limitations

Documented honestly rather than glossed over:

- **Admin routes have authentication but the difficulty-adaptation system is batch-level, not truly real-time** — it can react to a *previous* completed interview's scores, not mid-interview within the same 5-question set, since all 5 questions are generated up front
- **One rare bug**: in specific follow-up/index-advance interaction sequences, a single answer can occasionally be double-counted in the evaluation step against two different questions. Low-frequency, does not crash the system, final scores remain directionally correct
- **Memory/topic labeling** (`user_memory.strong_areas`/`weak_areas`) currently stores truncated question text rather than clean extracted topic labels
- **No automated test suite yet** — all features were verified through manual testing (Swagger, curl, and the live UI) rather than pytest; the `tests/` directory exists but is currently empty
- **TTS quota**: Groq's free-tier daily token limit for Orpheus TTS is modest (~3600 tokens/day) and can be exhausted during heavy testing sessions

---
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
## Acknowledgments

Built by Shrayans Kumar, B.Tech Electrical Engineering, NIT Rourkela, as a placement portfolio project.


