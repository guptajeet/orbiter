# Orbiter Deployment & Operations Todo Guide

Use this interactive file to track your progress, note issues, and log comments as you configure and launch the Orbiter platform.

## Legend / Status Codes
- `[ ]` **TODO**: Task not started yet
- `[/]` **IN PROGRESS**: Currently working on this task
- `[x]` **DONE**: Task successfully completed
- `[!]` **ISSUE**: Blocked or encountered an issue (describe in the *Comments/Issues* column)

---

## 📋 Phase 1: Environment & Secrets Setup

| Status | Task | Description | Comments / Issues / Notes |
| :---: | :--- | :--- | :--- |
| `[ ]` | **Copy `.env.example`** | Run `cp orbiter/.env.example orbiter/.env` to create your local environment file. | |
| `[ ]` | **Configure AI Keys** | Open `.env` and fill in API keys for the providers you want to use (e.g. `GEMINI_API_KEY`, `GROQ_API_KEY`, etc.). | |
| `[ ]` | **Configure Job Board API Keys** | Set up `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, or `JSEARCH_API_KEY` to enable ingestion. | |
| `[ ]` | **Set up Gmail API Credentials** | 1. Go to Google Cloud Console.<br>2. Enable Gmail API.<br>3. Create OAuth Credentials.<br>4. Enter `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET` in `.env`. | |
| `[ ]` | **Set up Generic SMTP (Optional)** | Fill in `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, and `SMTP_PASSWORD` if using SMTP channels. | |

---

## 📋 Phase 2: Local Setup & Launch

| Status | Task | Command / Instructions | Comments / Issues / Notes |
| :---: | :--- | :--- | :--- |
| `[ ]` | **Create Virtual Env & Install Backend Deps** | Go to `orbiter/backend/` and run:<br>`python -m venv venv`<br>`venv\Scripts\activate` *(Windows)*<br>`pip install -r requirements.txt` | |
| `[ ]` | **Initialize Database** | Run FastAPI API server once (`python main.py`) to auto-create SQLite tables in `orbiter.db`. | |
| `[ ]` | **Perform OAuth Flow** | Trigger the first email-related action to run `InstalledAppFlow` and authorize Gmail access. This generates `token.json`. | |
| `[ ]` | **Install Dashboard Dependencies** | Go to `orbiter/dashboard/` and run:<br>`npm install` | |
| `[ ]` | **Start Redis Server** | Make sure Redis is installed and running on `localhost:6379`. | |
| `[ ]` | **Start Celery Worker** | Run from `orbiter/backend/`:<br>`celery -A backend.tasks.celery_app worker --loglevel=info` | |
| `[ ]` | **Start Development Servers** | **Backend**: `python main.py` in `backend/`<br>**Frontend**: `npm run dev` in `dashboard/` | |

---

## 📋 Phase 3: Docker Deployment (Alternative to Phase 2)

| Status | Task | Command / Instructions | Comments / Issues / Notes |
| :---: | :--- | :--- | :--- |
| `[ ]` | **Verify Docker & Docker Compose** | Ensure Docker Desktop is installed and running. | |
| `[ ]` | **Build & Launch Stack** | Run from `orbiter/` directory:<br>`docker-compose up --build` | |
| `[ ]` | **Verify Running Services** | Confirm Backend is at `http://localhost:8000/docs` and Dashboard is at `http://localhost:3000`. | |

---

## 📋 Phase 4: E2E Verification & Feature Check

| Status | Task | Verification Steps | Comments / Issues / Notes |
| :---: | :--- | :--- | :--- |
| `[ ]` | **Dashboard Navigation** | Open dashboard and check all routes (`Dashboard`, `Jobs`, `Applications`, `CRM`, `Analytics`, `Operations`, `Settings`). | |
| `[ ]` | **Run Unit Test Suite** | Verify tests pass locally:<br>`python -m pytest tests/ -v` | |
| `[ ]` | **Run Chaos Suite** | Run resilience tests:<br>`python -c "from backend.chaos.module import ChaosModule; ChaosModule().run_resilience_suite()"` | |
| `[ ]` | **Run Job Ingestion** | Trigger job ingestion from the dashboard or via manual trigger to fetch new jobs from configured plugins (Remotive, RSS, Adzuna). | |
| `[ ]` | **Evaluate Match Scoring** | Feed a test resume and job listing to ensure Match Engine returns score and matching analytics. | |
| `[ ]` | **Check Outreach Delivery** | Attempt sending a test follow-up outreach email. | |
