# Orbiter — Plans & Feature Ideas

A developer-friendly list of planned features, add-ons, and improvements. Pick any row and build it — everything is modular.

---

## 🔌 Data Sources (Job Discovery)

| Feature | Where to Hook In | API / Method | Notes |
|---------|-----------------|--------------|-------|
| Google Jobs | `backend/plugins/sources/` | SerpAPI or Brave Search API | Best signal quality, covers ATS portals |
| Indeed | `backend/plugins/sources/` | Indeed Publisher API or scraper | Largest volume |
| LinkedIn Jobs | `backend/plugins/sources/` | Playwright scraper + session cookie | High quality leads |
| Glassdoor | `backend/plugins/sources/` | Partner API or scraper | Also pulls company reviews |
| Wellfound (AngelList) | `backend/plugins/sources/` | Official API | Startup jobs |
| We Work Remotely | `backend/plugins/sources/` | RSS Feed | Remote-only roles |
| Dice.com | `backend/plugins/sources/` | Partner API | Tech-heavy roles |
| Greenhouse / Lever / Ashby | `backend/plugins/sources/` | SerpAPI `site:greenhouse.io` query | Direct ATS postings |
| Twitter/X Jobs | `backend/plugins/sources/` | Search API v2 | `#hiring` keyword stream |

---

## 📧 HR Email Discovery & Outreach

| Feature | Where to Hook In | API / Method | Notes |
|---------|-----------------|--------------|-------|
| Email discovery by company domain | `backend/agents/discovery/` | Hunter.io API | `company.com` → `hr@company.com` |
| Contact enrichment | `backend/agents/discovery/` | Apollo.io API | Name, title, LinkedIn |
| Email verification | `backend/agents/discovery/` | Snov.io or SMTP handshake | Don't send to dead emails |
| Careers page scraper | `backend/agents/discovery/` | Playwright | Many companies list HR email on `/careers` |
| AI-personalized cold email | `backend/agents/composition/` | LLM prompt | Use company + job + resume context |
| Daily batch email sending | `backend/tasks/outreach_tasks.py` | Gmail / SMTP plugin | Configurable limit per day |
| Open / reply tracking | `backend/plugins/channels/` | Tracking pixel or Mailgun webhooks | Know who opened |
| Bulk unsubscribe / cooldown | `config/outreach.yaml` | Config-driven | Don't email same company within N days |

---

## 🧠 AI / Composition Quality

| Feature | Where to Hook In | Method | Notes |
|---------|-----------------|--------|-------|
| Company enrichment before composing | `backend/agents/composition/` | SerpAPI + Apollo | Pull culture, tech stack, news before writing |
| Structured job requirement extraction | `backend/agents/intelligence/` | LLM prompt chain | Extract skills list, seniority, keywords |
| ATS keyword injection | `backend/agents/composition/` | Resume tailor agent | Ensure resume passes ATS scanners |
| Cover letter quality scoring | `backend/agents/intelligence/qa_agent.py` | LLM score 0–10, retry if < 7 | Already scaffolded, strengthen threshold |
| A/B test resume versions | `backend/evaluation/` | Already exists | Track which version gets more responses |
| Interview prep generator | `backend/agents/` (new) | LLM | Auto-generate likely questions when interview scheduled |
| Recruiter name personalisation | `backend/agents/composition/` | From CRM contact record | "Hi Sarah," instead of "Dear Hiring Manager" |

---

## ⚙️ Config & Automation Control

| Feature | Where to Hook In | Method | Notes |
|---------|-----------------|--------|-------|
| Live config editor in dashboard | `dashboard/src/pages/Settings.jsx` | Monaco Editor embed | Edit YAML configs from UI |
| Hot-reload configs without restart | `backend/api/settings.py` | `importlib.reload` or watchdog | Apply changes instantly |
| Automation level slider (0–10) | `config/automation_rules.yaml` + dashboard | Config flag | 0 = manual approve all, 10 = fully autonomous |
| Per-source enable/disable toggle | `config/job_sources.yaml` + dashboard | Config flag | Already in YAML, just needs UI toggle |
| Salary / location / company blocklist filters | `config/filters.yaml` (new file) | Config-driven | Skip jobs below salary threshold etc. |
| Multiple resume personas | `config/personas.yaml` (new file) | Config-driven | Different resume for "senior dev" vs "freelance" |
| Schedule editor | `config/schedules.yaml` + dashboard | Cron expression UI | Change when Celery Beat tasks fire |

---

## 🎨 UI / Frontend

| Feature | Where to Hook In | Method | Notes |
|---------|-----------------|--------|-------|
| Full dark theme design system | `dashboard/src/index.css` | CSS variables | Replace all inline styles |
| Landing / onboarding scroll page | `dashboard/src/pages/` (new) | React + scroll animations | First impression page for new users |
| Outreach Center page | `dashboard/src/pages/` (new) | React | Email campaign management UI |
| Job Kanban board upgrade | `dashboard/src/components/pipeline/` | React DnD | Drag between Discovered → Applied → Interview |
| Real-time WebSocket feed | `dashboard/src/` | FastAPI WebSocket endpoint | Live agent events without polling |
| Config panel page | `dashboard/src/pages/Settings.jsx` | Monaco Editor | Edit YAML from browser |
| Analytics upgrade | `dashboard/src/pages/Analytics.jsx` | Recharts / D3 | Response rate, funnel, A/B results |
| Mobile responsive layout | `dashboard/src/` | CSS Grid / Flexbox | Currently desktop-only |
| Micro-animations | Throughout | Framer Motion | Card hovers, count-ups, skeleton loaders |

---

## 🔔 Notifications

| Feature | Where to Hook In | Method | Notes |
|---------|-----------------|--------|-------|
| Telegram bot alerts | `backend/plugins/channels/` (new) | Telegram Bot API | Instant ping on interview invite / reply |
| Discord webhook | `backend/plugins/channels/` (new) | Discord Webhook API | Post daily digest to a channel |
| Browser push (PWA) | `dashboard/` | Web Push API + service worker | Make dashboard installable |
| Enhanced daily email digest | `backend/agents/reporting/digest_agent.py` | Improve HTML template | Richer HTML, charts embedded |

---

## 🚀 Hosting & Infrastructure

| Feature | Where to Hook In | Method | Notes |
|---------|-----------------|--------|-------|
| PostgreSQL (replace SQLite) | `backend/core/database.py` | SQLAlchemy URL swap | Required for production / concurrent writes |
| Docker production compose | `docker-compose.prod.yml` (new) | Docker Compose | PostgreSQL + Nginx + SSL |
| Nginx reverse proxy + SSL | `nginx/orbiter.conf` (new) | Certbot + Let's Encrypt | Free SSL, auto-renews |
| Oracle VPS / any Linux VPS deploy | `scripts/deploy.sh` (new) | Shell script | One-command deploy |
| DB backup script | `scripts/backup.sh` (new) | pg_dump + cron | Daily automated backup |
| CI/CD pipeline | `.github/workflows/` (new) | GitHub Actions | Auto-deploy on push to main |

---

## 🔐 Auth & Multi-User

| Feature | Where to Hook In | Method | Notes |
|---------|-----------------|--------|-------|
| JWT login / register | `backend/api/` + `backend/core/security.py` | Already scaffolded | Complete the endpoints |
| Per-user resume + config | `backend/models/user.py` | FK relationships | Each user has own settings |
| Role-based access (admin / viewer) | `backend/core/security.py` | JWT claims | Viewer can't change config |
| OAuth (Google login) | `backend/api/` | `authlib` library | One-click sign-in |

---

## 🧩 ATS Submission Integrations

| Platform | Where to Hook In | Method | Notes |
|----------|-----------------|--------|-------|
| Greenhouse | `backend/agents/execution/` | Greenhouse Jobs API | Programmatic apply |
| Lever | `backend/agents/execution/` | Lever API | Programmatic apply |
| Workday | `backend/agents/execution/` | Playwright form automation | No API — browser fill |
| LinkedIn Easy Apply | `backend/agents/execution/` | Playwright | Requires session cookie |

---

> **Note:** The plugin pattern for sources and channels is in `backend/plugins/`. Stick to that pattern when adding anything new — it keeps things clean and swappable. All config is in `config/*.yaml`.
