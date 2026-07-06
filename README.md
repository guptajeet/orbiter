# Orbiter — Mission Control Job Automation Platform

Orbiter is an autonomous job discovery, matching, composition, application submission, and CRM follow-up manager. It operates as a multi-agent system coordinating ingestion, matching, tailoring, submission, and status monitoring.

## System Architecture

The platform uses a hierarchical multi-agent framework:
- **Master Orchestrator**: Manages general sessions, queues, and task routing.
- **Ingestion Supervisor**: Discovers jobs via API, scrapers, and recruiter emails.
- **Intelligence Supervisor**: Normalizes resumes, evaluates role fits, and monitors quality.
- **Composition Supervisor**: Tailors resumes and generates custom cover letters.
- **Execution Supervisor**: Submits applications via APIs or browser automation and tracks statuses.
- **Reporting Supervisor**: Formulates daily digests and triggers critical notifications.

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.13+ (if running locally without Docker)
- Node.js 18+ & npm (if running frontend locally)
- Redis 5.0+ (bundled in `redis/` folder for Windows)

### Configuration
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Enter your API credentials (e.g. `GEMINI_API_KEY`, `GROQ_API_KEY`, etc.) in `.env`.

### Run via Docker Compose
To launch the entire stack (FastAPI Backend, Redis, Celery workers, and React Dashboard):
```bash
docker-compose up --build
```
The dashboard will be available at `http://localhost:3000` and the API server at `http://localhost:8000`.

### Run Locally (Windows Quick Start)
To start all services natively on Windows in a single step, you can either:
* **Double-Click Launcher**: Double-click the `Double-Click-To-Start-Orbiter.bat` file.
* **Single Terminal Command**: Run the unified process manager:
  ```powershell
  python start_orbiter.py
  ```

This automatically flushes stale Redis tasks, boots Redis, Celery worker (with Windows thread pooling), Celery Beat, FastAPI, and Vite React dev server, running the entire stack in a single window. Open `http://localhost:5173` to access the dashboard. Press `Ctrl+C` to shut down all processes cleanly.

### Run Locally (Manual Terminal Mode)
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
2. **Workers**:
   ```bash
   cd backend
   celery -A backend.tasks.celery_app worker --loglevel=info --pool=threads
   ```
3. **Dashboard**:
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```

---

## Directory Structure
- `backend/`: FastAPI API, agents, adapters, plugins, models, and tasks.
- `dashboard/`: Vite React application.
- `config/`: YAML-driven settings, rules, and prompt templates.
- `prompts/`: Versioned seed prompts for the PromptOps database.
- `tests/`: Complete pytest verification suite.
