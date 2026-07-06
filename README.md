<div align="center">

# 🛸 Orbiter

### Autonomous Job Search Mission Control

**Orbiter is a self-operating, multi-agent AI platform that discovers jobs, scores your fit, tailors your resume and cover letter, submits applications, and manages recruiter follow-ups — all on autopilot.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61dafb?logo=react)](https://react.dev)
[![Celery](https://img.shields.io/badge/Celery-5.x-37814A?logo=celery)](https://docs.celeryq.dev)
[![Redis](https://img.shields.io/badge/Redis-5.0+-red?logo=redis)](https://redis.io)

</div>

---

## What Is Orbiter?

Orbiter removes the manual grind from job searching. Once configured, it runs 24/7 as a pipeline of AI agents that:

1. **Ingest** — Continuously pulls fresh job listings from multiple job boards and APIs
2. **Match** — Scores each listing against your resume using LLM-powered analysis
3. **Compose** — Rewrites your resume and generates a personalised cover letter for every high-match job
4. **Execute** — Submits applications and tracks their status
5. **Report** — Sends you a daily digest of what happened and follows up with recruiters via email

> **The 5-second pitch:** Upload your resume → set your preferences → Orbiter finds jobs, applies, and follows up while you sleep.

---

## Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent Architecture** | Specialised supervisor agents for ingestion, intelligence, composition, execution, and reporting |
| 🧠 **AI-Powered Matching** | LLM scores resume-to-job fit with confidence tiers (high / medium / low / no-fit) |
| ✍️ **Resume & Cover Letter Tailoring** | Full job description read and rewritten per application |
| 📬 **Recruiter CRM** | Tracks every contact, conversation, and follow-up schedule |
| 🔌 **Plugin Architecture** | Swap AI providers (Gemini, Groq, Mistral, DeepSeek, OpenRouter…) and job sources without code changes |
| ⚙️ **Config-Driven** | Every behaviour controlled via YAML — no code edit needed for tuning |
| 📊 **React Dashboard** | Real-time agent timeline, application Kanban, analytics, and prompt ops |
| 🐳 **Docker Ready** | One command spins up the full stack |
| 🪟 **Windows Quick-Start** | Bundled Redis + single-click `.bat` launcher |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  React Dashboard                     │
│         (Vite + React 18, port 5173)                 │
└──────────────────────┬──────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────┐
│              FastAPI Backend (port 8000)              │
│  ┌──────────┐ ┌──────────┐ ┌────────────────────┐   │
│  │ API Layer│ │AI Gateway│ │  Plugin Manager    │   │
│  └──────────┘ └──────────┘ └────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │ Celery Tasks
┌──────────────────────▼──────────────────────────────┐
│               Celery Worker + Beat                    │
│  ┌────────────┐ ┌─────────────┐ ┌────────────────┐  │
│  │ Ingestion  │ │ Intelligence│ │  Composition   │  │
│  │ Supervisor │ │ Supervisor  │ │  Supervisor    │  │
│  └────────────┘ └─────────────┘ └────────────────┘  │
│  ┌────────────┐ ┌─────────────┐                      │
│  │ Execution  │ │  Reporting  │                      │
│  │ Supervisor │ │  Supervisor │                      │
│  └────────────┘ └─────────────┘                      │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼──────┐             ┌────────▼──────┐
│    Redis     │             │   SQLite DB   │
│  (Broker +   │             │  (orbiter.db) │
│   Results)   │             └───────────────┘
└──────────────┘
```

### Agent Responsibilities

| Agent | Role |
|-------|------|
| **Ingestion Supervisor** | Polls job boards (Adzuna, JSearch, Remotive, RSS), deduplicates listings, stores to DB |
| **Intelligence Supervisor** | Parses uploaded resumes, scores resume ↔ job fit, classifies confidence tiers |
| **Composition Supervisor** | Tailors resume bullet points and generates cover letters using full job description |
| **Execution Supervisor** | Submits applications via ATS APIs or browser automation, tracks status changes |
| **Reporting Supervisor** | Generates daily HTML email digest, triggers critical alerts |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI (Python 3.13+) |
| Task Queue | Celery 5 + Redis |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI Gateway | Gemini, Groq, Mistral, DeepSeek, OpenRouter, HuggingFace, Cerebras |
| Frontend | React 18 + Vite |
| Email | Gmail API + SMTP |
| Browser Automation | Playwright (for ATS form submission) |
| Containerisation | Docker + Docker Compose |

---

## Getting Started

### Prerequisites

| Requirement | Version | Notes |
|------------|---------|-------|
| Python | 3.13+ | Backend runtime |
| Node.js | 18+ | Dashboard dev server |
| Redis | 5.0+ | Bundled in `redis/` for Windows |
| Docker | Latest | Optional, for containerised run |

### 1. Clone the Repository

```bash
git clone https://github.com/guptajeet/orbiter.git
cd orbiter
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

```env
# AI Provider (at least one required)
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Email (for outreach and digest)
GMAIL_ADDRESS=you@gmail.com
GMAIL_APP_PASSWORD=your_app_password

# Job Source APIs
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
```

> See `.env.example` for the full list of configurable keys.

### 3. Run the Stack

#### Option A — Docker (Recommended)
```bash
docker-compose up --build
```
- Dashboard → `http://localhost:5173`
- API → `http://localhost:8000`
- API Docs → `http://localhost:8000/docs`

#### Option B — Windows One-Click
Double-click `Double-Click-To-Start-Orbiter.bat`

This auto-boots Redis, Celery worker, Celery Beat, FastAPI, and Vite in a single terminal window.

#### Option C — Manual (Linux / macOS / Windows)

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python main.py

# Terminal 2 — Celery Worker
cd backend
celery -A backend.tasks.celery_app worker --loglevel=info --pool=threads

# Terminal 3 — Celery Beat (scheduler)
cd backend
celery -A backend.tasks.celery_app beat --loglevel=info

# Terminal 4 — Dashboard
cd dashboard
npm install
npm run dev
```

---

## Configuration

All behaviour is driven by YAML files in the `config/` directory — no code changes needed for day-to-day tuning.

| File | Controls |
|------|---------|
| `config/job_sources.yaml` | Which job boards to poll, priority order, rate limits |
| `config/ai_providers.yaml` | Which LLM for which task, fallback chain |
| `config/automation_rules.yaml` | Auto-apply thresholds, approval gates |
| `config/schedules.yaml` | Cron timing for all background tasks |
| `config/digest.yaml` | Daily email digest format and timing |
| `config/plugins.yaml` | Active email channels and source plugins |

---

## Project Structure

```
orbiter/
├── backend/
│   ├── agents/            # Multi-agent logic (ingestion, intelligence, composition, execution, reporting)
│   ├── api/               # FastAPI route handlers
│   ├── ai_gateway/        # Unified LLM gateway with provider switching
│   ├── core/              # DB session, config loader, event bus, security
│   ├── crm/               # Recruiter contact management and follow-up engine
│   ├── evaluation/        # A/B testing, feedback loops, analytics
│   ├── memory/            # Application memory and decay logic
│   ├── models/            # SQLAlchemy ORM models
│   ├── plugins/           # Swappable source, channel, and provider plugins
│   ├── promptops/         # Prompt versioning, experimentation, and migration
│   ├── services/          # Email, job, match, and profile services
│   ├── tasks/             # Celery task definitions
│   └── utils/             # Shared utilities (PDF parser, dedup, embedding, etc.)
├── dashboard/             # React + Vite frontend
├── config/                # YAML configuration files
├── prompts/               # Versioned LLM prompt templates
├── tests/                 # Pytest test suite
├── docs/                  # Planning and design documents
├── scripts/               # Helper scripts (healthcheck, deploy)
├── redis/                 # Bundled Redis binaries (Windows)
├── docker-compose.yml     # Full stack container setup
├── start_orbiter.py       # Windows unified process launcher
├── PLANS.md               # Feature roadmap and developer add-on guide
└── USER_GUIDE.md          # End-user setup and usage documentation
```

---

## API Reference

Interactive API docs available at `http://localhost:8000/docs` (Swagger UI) when the backend is running.

Key endpoint groups:

| Prefix | Description |
|--------|-------------|
| `/api/jobs` | Browse, filter, and trigger job ingestion |
| `/api/applications` | View and manage applications |
| `/api/profile` | Upload and manage resume profile |
| `/api/crm` | Recruiter contacts and follow-up schedules |
| `/api/settings` | Read and update configuration |
| `/api/analytics` | Match rates, response rates, agent metrics |
| `/api/health` | System health check |

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

---

## Contributing & Future Plans

See [PLANS.md](PLANS.md) for a full developer-friendly table of planned features, add-ons, and known improvements — each with the exact file to hook into and the API/library to use.

---

## License

This project is licensed under the [MIT License](LICENSE).
