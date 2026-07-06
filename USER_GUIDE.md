# Orbiter — Complete User Guide

## What Is Orbiter?

Orbiter is an AI-powered job search automation platform. It discovers jobs, scores how well they match your resume, generates tailored resumes and cover letters, tracks your applications, and manages recruiter relationships — all from a single dashboard.

**The 5-second version:** Upload your resume → Orbiter finds jobs → AI scores each match → You approve or reject → Orbiter applies and tracks everything.

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.13+ |
| Node.js | 18+ |
| Redis | 5.0+ (bundled in `redis/` folder) |
| Browser | Any modern browser (Chrome recommended) |

---

## Starting the System

### Method 1: The Quick Double-Click Launcher (Recommended for Non-Coders)
Simply double-click the `Double-Click-To-Start-Orbiter.bat` file in the project root directory. This will automatically:
1. Locate and start the native Windows Redis server in the background.
2. Launch the FastAPI backend server.
3. Start the Celery Worker with Windows-compatible thread pooling.
4. Start the Celery Beat scheduler.
5. Launch the Vite React frontend dev server.
This launches everything in one console window. Open **`http://localhost:5173`** to access the dashboard. Press `Ctrl+C` in that console to shut down all services.

### Method 2: Single Terminal Command Launcher
If you prefer using the terminal but want to launch all services at once, run:
```powershell
python start_orbiter.py
```
This flushes stale task queues and boots up Redis, FastAPI, Celery, and Vite together. Open **`http://localhost:5173`** to access the dashboard. Press `Ctrl+C` to cleanly terminate all processes.

### Method 3: Manual Multi-Terminal Launch (Advanced / Debugging)
Open **5 separate terminals** and run these commands in order:

#### Terminal 1 — Redis (start first)
```
cd K:\JOB\orbiter
K:\JOB\orbiter\redis\redis-server.exe K:\JOB\orbiter\redis\redis.windows.conf
```
Wait until you see `Ready to accept connections`. This must stay running.

#### Terminal 2 — Backend API Server
```
cd K:\JOB\orbiter
set PYTHONPATH=K:\JOB\orbiter && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Wait until you see `Uvicorn running on http://0.0.0.0:8000`.

#### Terminal 3 — Celery Worker (processes background tasks)
```
cd K:\JOB\orbiter
python -m celery -A backend.tasks.celery_app worker --loglevel=info --pool=threads
```
Wait until you see `celery@... ready.`

#### Terminal 4 — Celery Beat (scheduler)
```
cd K:\JOB\orbiter
python -m celery -A backend.tasks.celery_app beat --loglevel=info
```
Wait until you see `beat: Starting...`

#### Terminal 5 — Frontend Dashboard
```
cd K:\JOB\orbiter\dashboard
npm run dev
```
Open the URL shown (usually `http://localhost:5173`).

### One-Time: Gmail Email Monitoring Setup
```
cd K:\JOB\orbiter
python setup_gmail.py
```
A browser window opens. Sign in with your Google account and authorize. After that, email monitoring works automatically.

---

## Stopping the System

If running via Method 1 or Method 2, simply press `Ctrl+C` in the launcher console and confirm (if prompted) to shut everything down.

If running via Method 3 (manual multi-terminal mode), close all 5 terminal windows, or run:
```
# In PowerShell:
Get-Process python,redis-server,node -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## Dashboard Overview

The dashboard has **8 pages** accessible from the left sidebar:

| Page | What It Does |
|------|-------------|
| Dashboard | System health, stats overview, agent activity feed |
| Quick Start Guide | Step-by-step onboarding walkthrough |
| Jobs Explorer | View discovered jobs, trigger discovery, apply manually |
| Applications | Kanban board of all your applications, approve/reject pipeline |
| Recruiter CRM | Track recruiter contacts, conversations, follow-ups |
| Analytics & Eval | Performance reports, raw metrics, prompt management |
| Operations | Switch automation modes (Advisor/Copilot/Autopilot), chaos testing |
| Settings | Upload resume, configure profile, set workflow rules |

---

## Step-by-Step Usage

### Step 1: Set Up Your Profile

**Go to Settings page**

1. **Upload your resume** — Drag and drop a PDF, DOCX, or TXT file into the upload area. The system extracts your text and uses AI to parse your skills, experience, and education.

2. **Enter your email** — Type your primary email address (comma-separated if you have multiple).

3. **Add LinkedIn URL** — Paste your LinkedIn profile URL.

4. **Add Indeed URL** (optional) — Paste your Indeed profile URL.

5. Click **Save Profile**.

### Step 2: Configure Automation Rules

**Still on Settings page, scroll to Workflow Rules**

| Setting | What It Does | Recommended |
|---------|-------------|-------------|
| Confidence Threshold | Minimum match score (50-95%) before auto-apply kicks in | 80% |
| Automation Mode | Advisor / Copilot / Autopilot (see below) | Copilot |
| Job Discovery Interval | How often to scan for new jobs (minutes) | 60 |
| Auto-Apply | Automatically submit to jobs above threshold | Off (start with Copilot) |
| Email Monitoring | Check Gmail for interview invites and recruiter replies | On |

### Step 3: Understand Automation Modes

| Mode | What It Does | You Need To... |
|------|-------------|----------------|
| **Advisor** | Discovers and scores jobs only | Review everything yourself |
| **Copilot** | Discovers, scores, generates resumes + cover letters | Approve each application before submit |
| **Autopilot** | Full autonomous — applies to high-confidence matches automatically | Monitor the dashboard |

**How to switch:** Go to Operations page → click the mode card you want.

### Step 4: Discover Jobs

**Go to Jobs Explorer page**

1. Click **Discover Jobs** button.
2. The system searches Adzuna, JSearch, Remotive, and RSS feeds.
3. Jobs appear in the list as they are found.
4. Click any job to see full details: title, company, location, salary, description, required skills.

**What happens behind the scenes:**
- AI scores each job against your resume (0.0 to 1.0)
- Jobs are tagged with domain (backend, frontend, data science)
- Duplicate jobs are automatically removed
- Each match gets a confidence tier: high, medium, low, or no-fit

### Step 5: Review and Apply

**Go to Applications page**

The Applications board is a Kanban with 5 columns:

| Column | Status | What To Do |
|--------|--------|-----------|
| Review Needed | `pending_approval` | Click card → review tailored resume + cover letter → Approve or Reject |
| Applied | `submitted` | Already submitted, waiting for response |
| Interview | `interview` | You got an interview! |
| Rejected | `rejected` | Not selected |
| Offer | `offer` | You got an offer! |

**To approve an application:**
1. Click the application card in "Review Needed"
2. A modal opens showing:
   - Job details
   - Tailored resume (AI-optimized for this specific job)
   - Cover letter
   - Tracking events
3. Click **Approve** — the system submits your application
4. Click **Reject** — the application is marked rejected

**To apply manually:**
1. Go to Jobs Explorer
2. Click a job
3. Click **Apply to This Job**
4. Go to Applications to approve it

### Step 6: Manage Recruiter Contacts

**Go to Recruiter CRM page**

**Add a contact:**
1. Click **+ Add Contact**
2. Fill in: Name, Email, Company, Title
3. Click Save

**Log a conversation:**
1. Select a contact from the left panel
2. The conversation appears on the right
3. Messages are logged as inbound or outbound

**Relationship score:**
- Each contact has a score (0.0 to 1.0) based on their response rate
- Green (>= 0.8): Strong relationship
- Yellow (0.5 - 0.79): Developing
- Red (< 0.5): Weak or no response

**Follow-ups:**
- The system automatically schedules follow-ups based on conversation activity
- Follow-up emails are sent after 72 hours of no response (configurable)

### Step 7: Monitor Performance

**Go to Analytics & Eval page**

**Report tab:**
- Match Precision: How accurate the AI scoring is
- Callback Rate: Percentage of applications that get responses
- Email Response Rate: Percentage of outreach emails that get replies

**Raw Metrics tab:**
- Paginated table of every metric recorded
- Filter by metric name, sort by timestamp

### Step 8: Manage AI Prompts

**Go to Analytics & Eval → PromptConsole component**

Orbiter uses 8 AI prompts that you can customize:

| Prompt | Purpose |
|--------|---------|
| match_scorer | Scores job-resume fit |
| resume_parser | Extracts structured data from resume |
| resume_tailor | Tailors resume for specific job |
| cover_letter | Generates cover letters |
| outreach_email | Cold outreach to recruiters |
| followup_email | Follow-up on applications |
| daily_digest | Compiles daily status email |
| qa_verification | Detects AI hallucinations |

**To create a new version:**
1. Click a prompt name
2. Click **Create New Version**
3. Edit the content (use `{{variable_name}}` for dynamic values)
4. Click Save
5. Click **Activate** to make it the live version

**To rollback:**
- Click **Rollback** on any previous version to revert

---

## Background Tasks (Automatic)

Once Redis + Celery are running, these tasks execute automatically:

| Task | Frequency | What It Does |
|------|-----------|-------------|
| Email Monitoring | Every 5 minutes | Checks Gmail for interview invites, logs urgent alerts |
| Job Discovery | Every 2 hours | Scans job boards for new listings |
| Follow-up Check | Every 1 hour | Sends follow-up emails to recruiters who haven't responded |
| Daily Digest | Every 24 hours | Compiles and sends daily status email |

**To trigger tasks manually:**
- Email check: `POST /api/email/check` (or click in Settings)
- Job discovery: Click "Discover Jobs" on Jobs page

---

## Email Monitoring Setup (Detailed)

### Gmail OAuth (for reading inbox)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select existing)
3. Enable the **Gmail API**
4. Go to APIs & Services → Credentials
5. Create **OAuth 2.0 Client ID** → Application type: **Desktop app**
6. Copy the Client ID and Client Secret into your `.env` file:
   ```
   GMAIL_CLIENT_ID=your_client_id_here
   GMAIL_CLIENT_SECRET=your_client_secret_here
   ```
7. Run: `python setup_gmail.py`
8. Browser opens → sign in → authorize → done

### SMTP (for sending emails)

Your `.env` already has SMTP configured (Brevo). This is used for:
- Sending cover letters
- Recruiter outreach emails
- Follow-up emails
- Daily digest emails

---

## Configuration Files

All config files are in `config/`:

| File | Controls |
|------|----------|
| `default.yaml` | Database URL, Redis URL, daily limits, log level |
| `ai_providers.yaml` | AI provider API keys, model names, function routing |
| `job_sources.yaml` | Which job boards to search, API credentials |
| `automation_rules.yaml` | Mode definitions (advisor/copilot/autopilot), thresholds |
| `plugins.yaml` | Which plugins are enabled |
| `schedules.yaml` | Task intervals (seconds) |
| `digest.yaml` | Daily digest email settings |
| `domain_taxonomy.yaml` | Job domains and skill classifications |
| `ats_adapters.yaml` | ATS platform configurations |
| `chaos_scenarios.yaml` | Chaos testing scenarios |

---

## AI Providers

Orbiter tries providers in this order (with automatic fallback):

| Function | Primary | Fallback 1 | Fallback 2 |
|----------|---------|-----------|-----------|
| Resume Parsing | Groq | DeepSeek | Gemini |
| Match Scoring | Groq | DeepSeek | Gemini |
| Resume Tailoring | Groq | DeepSeek | Gemini |
| Cover Letters | Groq | DeepSeek | Gemini |
| Embeddings | HuggingFace | — | — |

If one provider hits rate limits or goes down, the system automatically tries the next.

---

## Troubleshooting

### "No jobs found"
- Check that Adzuna/JSearch API keys are set in `.env`
- Click "Discover Jobs" manually
- Check backend terminal for error messages

### "Applications stuck in Review Needed"
- Go to Applications page
- Click the card and click Approve

### "Email monitoring not working"
- Run `python setup_gmail.py` to authenticate
- Check `GET /api/email/status` shows `"gmail_configured": true`
- Ensure Celery Worker is running

### "Background tasks not executing"
- Ensure Redis is running (`redis-cli ping` should return `PONG`)
- Ensure Celery Worker is running (should show `celery@... ready.`)
- Ensure Celery Beat is running (should show `beat: Starting...`)

### "AI responses are poor quality"
- Go to Analytics → PromptConsole
- Create a new version of the relevant prompt
- Test different phrasings

### "Frontend shows blank data"
- Check backend is running on port 8000
- Check browser console for API errors
- Ensure `PYTHONPATH=K:\JOB\orbiter` is set when starting backend

---

## API Reference (All Endpoints)

### Health & System
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | System health check |
| GET | `/api/settings` | Get all settings |
| PUT | `/api/settings` | Update settings |
| GET | `/api/mode` | Get automation mode |
| PUT | `/api/mode` | Switch automation mode |

### Profile & Resume
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/profile` | Get user profile |
| POST | `/api/profile` | Save user profile |
| POST | `/api/profile/resume` | Upload resume file |

### Jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/jobs` | List jobs (paginated) |
| GET | `/api/jobs/{id}` | Get job details |
| POST | `/api/jobs/discover` | Trigger job discovery |
| POST | `/api/jobs/{id}/apply` | Create manual application |

### Applications
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/applications` | List applications |
| GET | `/api/applications/{id}` | Get application details |
| POST | `/api/applications/{id}/approve` | Approve application |
| POST | `/api/applications/{id}/reject` | Reject application |

### CRM
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/crm/contacts` | List recruiter contacts |
| POST | `/api/crm/contacts` | Add contact |
| GET | `/api/crm/contacts/{id}` | Get contact details |
| GET | `/api/crm/conversations/{id}` | Get conversation messages |
| POST | `/api/crm/conversations/{id}/messages` | Log a message |

### Email
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/email/check` | Trigger email check now |
| GET | `/api/email/status` | Check Gmail auth status |

### Analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/evaluation/report` | Get performance report |
| GET | `/api/evaluation/metrics` | List raw metrics |

### PromptOps
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/promptops/prompts` | List all prompts + versions |
| POST | `/api/promptops/prompts` | Create new prompt version |
| POST | `/api/promptops/prompts/{name}/activate/{id}` | Activate a version |
| POST | `/api/promptops/prompts/{name}/rollback` | Rollback to previous |

### Chaos Testing
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/chaos/scenarios` | List chaos scenarios |
| POST | `/api/chaos/scenarios/{name}/enable` | Enable scenario |
| POST | `/api/chaos/scenarios/{name}/disable` | Disable scenario |
| POST | `/api/chaos/run-suite` | Run full resilience test |

### Dashboard
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/dashboard/metrics` | Get dashboard stats |
| GET | `/api/dashboard/activity` | Get agent activity log |

---

## Project File Structure

```
orbiter/
├── .env                    # API keys and secrets (DO NOT COMMIT)
├── orbiter.db              # SQLite database
├── token.json              # Gmail OAuth token
├── redis/                  # Redis server (bundled)
├── setup_gmail.py          # One-time Gmail OAuth setup
├── backend/
│   ├── main.py             # FastAPI server entry point
│   ├── core/               # Config, database, security, events
│   ├── models/             # Database table definitions
│   ├── api/                # REST API endpoints (10 routers)
│   ├── agents/             # AI agents (5 supervisors, 12 agents)
│   ├── services/           # Business logic layer
│   ├── tasks/              # Celery background tasks
│   ├── plugins/            # Job sources, AI providers, email channels
│   ├── adapters/           # ATS application submission adapters
│   ├── ai_gateway/         # Multi-provider AI with failover
│   ├── crm/                # Recruiter relationship management
│   ├── evaluation/         # Metrics tracking and reporting
│   ├── promptops/          # Prompt version management
│   ├── chaos/              # Resilience testing
│   ├── memory/             # Agent memory (ChromaDB + SQLite)
│   └── utils/              # PDF parsing, validation, dedup
├── dashboard/
│   ├── src/
│   │   ├── App.jsx         # Router (9 routes)
│   │   ├── pages/          # 8 page components
│   │   └── components/     # Reusable UI components
│   └── package.json
├── config/                 # YAML configuration files (11 files)
├── prompts/                # AI prompt templates (8 files)
└── tests/                  # Test suite
```

---

## Database Tables (16 total)

| Table | Purpose |
|-------|---------|
| `user_profiles` | Your profile (email, LinkedIn, preferences) |
| `resume_profiles` | Uploaded resumes (raw text + parsed data) |
| `job_listings` | Discovered job postings |
| `match_results` | AI-generated match scores per job |
| `applications` | Your job applications with status |
| `action_logs` | Every action taken by every agent |
| `recruiter_contacts` | CRM contact records |
| `crm_conversations` | Conversation threads per contact |
| `followup_schedules` | Automated follow-up schedules |
| `evaluation_metrics` | Performance metrics |
| `experiment_results` | A/B test results |
| `prompt_versions` | Versioned AI prompts |
| `prompt_experiments` | Prompt A/B experiments |
| `agent_memories` | Agent learning memories |

---

## Quick Reference Card

| Action | Where |
|--------|-------|
| Upload resume | Settings → Resume/CV section |
| Save profile | Settings → User Profile → Save Profile |
| Discover jobs | Jobs Explorer → Discover Jobs button |
| Apply to a job | Jobs Explorer → click job → Apply to This Job |
| Approve application | Applications → click card → Approve |
| Reject application | Applications → click card → Reject |
| Add recruiter | CRM → + Add Contact |
| Log message | CRM → select contact → type message |
| Switch mode | Operations → click mode card |
| Check email now | Settings → Email section |
| Edit prompts | Analytics → PromptConsole |
| Run chaos tests | Operations → ChaosConsole |
| View metrics | Analytics → Report or Raw Metrics |
| Check system health | Dashboard → health indicator (top) |
