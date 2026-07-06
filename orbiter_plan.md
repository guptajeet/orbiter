# Orbiter — Mission Control Job Automation Platform (Final Architecture)

## Overview

**Orbiter** is a production-grade, multi-agent AI-powered platform that automates the entire job search lifecycle. It runs 24/7 autonomously with configurable automation modes, learns from every interaction, and reports via daily email digests.

This final architecture incorporates 9 major enhancements that elevate Orbiter from an MVP to a small SaaS-grade system.

---

## Architecture Enhancements Summary

| # | Enhancement | Impact |
|---|-----------|--------|
| 1 | **ATS Adapter Layer** | Clean abstraction for Greenhouse/Lever/Ashby/Workday — decoupled from agents |
| 2 | **Recruiter CRM** | Contacts, conversations, follow-ups, relationship scoring |
| 3 | **Evaluation Framework** | Match precision, callback rate, resume quality, email response rate tracking |
| 4 | **Agent Memory** | Agents learn from approvals/rejections/interactions over time |
| 5 | **Automation Modes** | Advisor → Copilot → Autopilot — switchable from dashboard |
| 6 | **PromptOps Subsystem** | Prompt versioning, A/B experiments, rollback, performance metrics |
| 7 | **Chaos Testing Module** | Failure simulator to validate resilience and fallback chains |
| 8 | **Plugin Architecture** | Drop-in support for new job boards, AI providers, outreach channels |
| 9 | **Enhanced Dashboard** | True mission control — timelines, agent traces, decision explanations, heatmaps, replays |

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ORBITER MISSION CONTROL                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐   ┌───────────────┐   ┌────────────────────────┐  │
│  │ Mission Control   │◄─►│ FastAPI       │◄─►│ Redis Event Bus        │  │
│  │ Dashboard (React) │   │ Backend       │   │ + Celery Workers       │  │
│  │                   │   │               │   │ + Celery Beat (24/7)   │  │
│  │ • Agent Timeline  │   └───────┬───────┘   └───────────┬────────────┘  │
│  │ • Decision Traces │           │                       │               │
│  │ • Confidence Maps │   ┌───────▼───────────────────────▼────────┐     │
│  │ • Workflow Replay │   │          MASTER ORCHESTRATOR            │     │
│  │ • Recruiter CRM   │   │   ┌─────────────────────────────────┐  │     │
│  │ • Mode Switcher   │   │   │     AUTOMATION MODE ENGINE      │  │     │
│  │ • Eval Metrics    │   │   │  Advisor ↔ Copilot ↔ Autopilot  │  │     │
│  │ • Chaos Controls  │   │   └─────────────────────────────────┘  │     │
│  └──────────────────┘   └──┬────────┬────────┬────────┬───────┬──┘     │
│                             │        │        │        │       │         │
│              ┌──────────────▼─┐ ┌────▼───┐ ┌──▼─────┐ ┌▼──────┴──┐     │
│              │  INGESTION     │ │ INTEL  │ │ COMP.  │ │ EXECUTION │     │
│              │  SUPERVISOR    │ │ SUPERV │ │ SUPERV │ │ SUPERVISOR│     │
│              └──┬──┬──┬──┬──┘ └┬──┬──┬┘ └┬──┬──┬┘ └┬──┬──┬──┘     │
│                 │  │  │  │     │  │  │    │  │  │    │  │  │        │
│              Workers...      Workers...  Workers... Workers...      │
│                                    │                   │            │
│                              ┌─────▼─────┐    ┌───────▼────────┐   │
│                              │  AGENT    │    │  ATS ADAPTER   │   │
│                              │  MEMORY   │    │  LAYER         │   │
│                              │  STORE    │    │  ┌───────────┐ │   │
│                              └───────────┘    │  │Greenhouse │ │   │
│                                               │  │Lever      │ │   │
│  ┌────────────┐ ┌────────────┐ ┌───────────┐  │  │Ashby      │ │   │
│  │ REPORTING  │ │ RECRUITER  │ │ EVAL      │  │  │Workday    │ │   │
│  │ SUPERVISOR │ │ CRM        │ │ FRAMEWORK │  │  │[Plugins]  │ │   │
│  │ E1 Digest  │ │ Contacts   │ │ Precision │  │  └───────────┘ │   │
│  │ E2 Analytx │ │ Convos     │ │ Callback  │  └────────────────┘   │
│  │ E3 Alerts  │ │ Follow-ups │ │ Quality   │                       │
│  └────────────┘ │ Rel.Score  │ │ Response  │                       │
│                 └────────────┘ └───────────┘                       │
│                                                                     │
│  ┌───────────────┐ ┌──────────────┐ ┌───────────────────────────┐  │
│  │ AI GATEWAY    │ │ PROMPTOPS    │ │ PLUGIN MANAGER            │  │
│  │ 8 Providers   │ │ Versioning   │ │ Sources │ Providers │ Ch. │  │
│  │ 2 Backups ea. │ │ Experiments  │ │ [drop-in registration]    │  │
│  │ Rate Limiting │ │ Metrics      │ └───────────────────────────┘  │
│  └───────────────┘ └──────────────┘                                │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ KNOWLEDGE BASE: SQLite + ChromaDB + Agent Memory + Config     │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────┐                          │
│  │ CHAOS TESTING MODULE (dev/staging)   │                          │
│  │ API failures │ AI timeouts │ Queue   │                          │
│  │ outages │ Rate limits │ Full chaos   │                          │
│  └──────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Enhancement 1: ATS Adapter Layer

Decouples ATS-specific logic from agents. Each ATS platform gets its own adapter that implements a common interface.

### Design

```python
# Abstract interface — all ATS adapters implement this
class BaseATSAdapter(ABC):
    def submit_application(self, application, resume, cover_letter) -> SubmissionResult
    def check_status(self, application_id) -> ApplicationStatus
    def get_form_fields(self, job_url) -> list[FormField]
    def fill_form(self, fields, profile_data) -> FilledForm
    def get_supported_features(self) -> list[str]
```

### Adapter Registry (config-driven)

```yaml
# config/ats_adapters.yaml
adapters:
  greenhouse:
    enabled: true
    adapter_class: "adapters.greenhouse.GreenhouseAdapter"
    auth_type: "api_key"
    features: ["api_submit", "status_check", "webhook"]
  lever:
    enabled: true
    adapter_class: "adapters.lever.LeverAdapter"
    auth_type: "api_key"
    features: ["api_submit", "status_check"]
  ashby:
    enabled: true
    adapter_class: "adapters.ashby.AshbyAdapter"
    auth_type: "api_key"
    features: ["api_submit"]
  workday:
    enabled: false  # V1 — requires browser automation
    adapter_class: "adapters.workday.WorkdayAdapter"
    auth_type: "browser_session"
    features: ["browser_submit"]
```

### Files

```
backend/adapters/
├── __init__.py
├── base.py                  # BaseATSAdapter ABC + SubmissionResult model
├── registry.py              # AdapterRegistry — loads from config, resolves by ATS type
├── greenhouse.py            # Greenhouse Candidate Ingestion API
├── lever.py                 # Lever Apply API
├── ashby.py                 # Ashby API
├── workday.py               # Workday browser-based adapter [V1]
└── generic_email.py         # Fallback: email-based submission
```

**Key principle**: The Execution Supervisor calls `adapter_registry.get_adapter(ats_type).submit_application(...)` — it never knows the ATS-specific details. New ATS platforms are added by implementing `BaseATSAdapter` and registering in YAML.

---

## Enhancement 2: Recruiter CRM

Lightweight CRM to track recruiter relationships, conversations, and follow-up effectiveness.

### Data Model

```
RecruiterContact
  |-- id, name, email, phone, linkedin_url
  |-- company, title, department
  |-- source (scraped | email_signature | linkedin | manual)
  |-- relationship_score (0.0 - 1.0, computed)
  |-- tags[], notes
  |-- first_contact_at, last_interaction_at
  |-- created_at, updated_at

Conversation
  |-- id, contact_id, application_id (nullable)
  |-- thread_id (Gmail thread reference)
  |-- messages[]: {direction: inbound|outbound, content, timestamp, sentiment}
  |-- status (active | dormant | closed)
  |-- next_followup_at

FollowUpSchedule
  |-- id, conversation_id, contact_id
  |-- trigger_type (time_based | event_based)
  |-- interval_hours (default: 72)
  |-- max_followups (default: 3)
  |-- current_count, last_sent_at
  |-- status (pending | sent | responded | exhausted)

RelationshipScore (computed)
  |-- engagement_frequency: How often they respond
  |-- response_rate: % of outreach that gets replies
  |-- response_latency: Average time to respond
  |-- sentiment_trend: Improving / declining / neutral
  |-- referral_potential: Based on seniority + engagement
  |-- overall_score: Weighted composite (0.0 - 1.0)
```

### Files

```
backend/crm/
├── __init__.py
├── models.py                # RecruiterContact, Conversation, FollowUpSchedule
├── service.py               # CRM service (CRUD, scoring, follow-up scheduling)
├── enrichment.py            # Auto-enrich contacts from email signatures, LinkedIn
├── scoring.py               # Relationship score computation
└── followup_engine.py       # Automated follow-up scheduling + execution

backend/api/
├── crm.py                   # CRM REST endpoints for dashboard
```

---

## Enhancement 3: Evaluation Framework

Tracks and measures the quality of every system decision to enable continuous improvement.

### Metrics Tracked

| Metric | How Measured | Used By |
|--------|-------------|---------|
| **Match precision** | % of high-confidence matches that result in callbacks | Match Engine tuning |
| **Callback rate** | % of submitted applications that receive any response | Overall system health |
| **Resume tailoring quality** | A/B test: original vs tailored resume response rates | Resume Tailor Agent |
| **Email response rate** | % of outreach emails that receive replies | Outreach Agent |
| **Cover letter effectiveness** | Callback rate for applications with vs without cover letters | Cover Letter Agent |
| **Follow-up conversion** | % of follow-ups that convert dormant to active conversations | CRM / Follow-up Engine |
| **Auto-apply accuracy** | % of auto-applied jobs the user would have also approved | Autopilot calibration |
| **Time-to-response** | Average time from application to first response | Pipeline health |
| **Source effectiveness** | Callback rate per job source (Adzuna vs JSearch vs email) | Source priority tuning |

### A/B Testing Framework

```python
class Experiment:
    name: str                    # e.g., "cover_letter_v2_vs_v3"
    variants: list[Variant]      # Each variant = a different prompt/template
    traffic_split: dict          # {"control": 0.5, "treatment": 0.5}
    metric: str                  # "callback_rate"
    min_sample_size: int         # Statistical significance threshold
    status: str                  # draft | running | concluded
    winner: str | None           # Determined when significant
```

### Files

```
backend/evaluation/
├── __init__.py
├── models.py                # EvaluationMetric, Experiment, ExperimentResult
├── tracker.py               # MetricsTracker — records outcomes per application
├── analyzer.py              # StatisticalAnalyzer — significance testing, trend detection
├── ab_testing.py            # ExperimentManager — A/B test lifecycle
├── reporter.py              # WeeklyEvaluationReport — generates insights
└── feedback_loop.py         # Feeds evaluation results back to agents for tuning
```

---

## Enhancement 4: Agent Memory

Persistent memory store that allows agents to learn from past interactions and improve over time.

### Memory Architecture

```
AgentMemory
  |-- id, agent_id, memory_type
  |-- content: JSON (structured memory data)
  |-- embedding: vector (for semantic retrieval)
  |-- relevance_score: float (decays over time)
  |-- created_at, last_accessed_at, access_count

Memory Types:
  - approval_pattern     → "User always approves roles at FAANG companies"
  - rejection_pattern    → "User rejects roles requiring 10+ years experience"
  - successful_variant   → "Resume version with 'cloud infrastructure' emphasis got 3 callbacks"
  - recruiter_preference → "Recruiter X responds faster to shorter emails"
  - company_insight      → "Company Y typically responds within 48 hours"
  - skill_mapping        → "User's 'FastAPI' experience maps well to 'backend development' roles"
  - outreach_style       → "Casual tone emails get 2x response rate vs formal"
```

### How Agents Use Memory

| Agent | Memory Usage |
|-------|-------------|
| **Match Engine** | Learns which match scores correlate with user approval; adjusts weights |
| **Resume Tailor** | Remembers which resume variants got callbacks; reuses successful patterns |
| **Cover Letter** | Learns which tone/structure gets responses per industry |
| **Outreach Agent** | Adapts email style based on recruiter response patterns |
| **Classification** | Learns user's actual domain boundary from approval/rejection history |
| **Master** | Learns optimal execution paths per job source and company type |

### Retrieval

```python
class MemoryStore:
    def remember(self, agent_id, memory_type, content, embedding=None)
    def recall(self, agent_id, query, memory_type=None, top_k=5) -> list[AgentMemory]
    def forget(self, agent_id, older_than_days=90)  # Memory decay
    def get_patterns(self, agent_id, memory_type) -> list[Pattern]
```

### Files

```
backend/memory/
├── __init__.py
├── models.py                # AgentMemory model
├── store.py                 # MemoryStore — CRUD + semantic retrieval via ChromaDB
├── patterns.py              # PatternExtractor — identifies recurring patterns
├── decay.py                 # MemoryDecay — relevance scoring + garbage collection
└── feedback.py              # FeedbackProcessor — converts user actions to memories
```

---

## Enhancement 5: Automation Modes

Three-tier automation system, switchable globally or per-agent from the dashboard.

### Mode Definitions

| Mode | Behavior | When to Use |
|------|----------|-------------|
| **🔍 Advisor** | Discovers jobs, scores matches, generates recommendations. **Never** composes or submits. Shows everything in dashboard + daily digest for user to act on manually. | First week — build trust, calibrate matching |
| **🤝 Copilot** | Discovers, scores, **composes** tailored resumes + cover letters. Queues everything for user approval before submission. Daily digest includes ready-to-send applications. | Weeks 2-4 — verify composition quality |
| **🚀 Autopilot** | Full autonomous operation. Auto-applies above confidence threshold. Only flags edge cases (low confidence, new company type, domain boundary) in digest. | After calibration — fire-and-forget |

### Configuration

```yaml
# config/automation_rules.yaml
automation_mode: "copilot"  # advisor | copilot | autopilot

mode_config:
  advisor:
    discover: true
    score: true
    compose: false
    submit: false
    outreach: false

  copilot:
    discover: true
    score: true
    compose: true
    submit: false          # queued for approval
    outreach: false        # queued for approval

  autopilot:
    discover: true
    score: true
    compose: true
    submit: true           # auto above threshold
    outreach: true         # auto above threshold
    confidence_threshold: 0.80
    daily_cap: 25
    
# Per-agent overrides (optional)
agent_overrides:
  outreach_agent:
    mode: "copilot"        # Always require approval for outreach even in autopilot
```

### Files

```
backend/core/
├── automation_mode.py       # AutomationModeEngine — resolves effective mode per action

backend/api/
├── mode.py                  # REST endpoints to switch modes from dashboard
```

---

## Enhancement 6: PromptOps Subsystem

Version-controlled prompt management with experimentation, rollback, and performance metrics.

### Design

```
PromptVersion
  |-- id, prompt_name (e.g., "cover_letter_generator")
  |-- version: int (auto-incrementing)
  |-- content: str (the full prompt template)
  |-- variables: list[str] (required template variables)
  |-- author: str
  |-- is_active: bool
  |-- performance_metrics: {avg_quality_score, avg_latency_ms, total_invocations, cost_per_call}
  |-- created_at

PromptExperiment
  |-- id, prompt_name
  |-- control_version_id, treatment_version_id
  |-- traffic_split: dict
  |-- metric: str (e.g., "callback_rate", "user_approval_rate")
  |-- status: draft | running | concluded
  |-- results: {control_score, treatment_score, p_value, winner}
```

### Capabilities

| Feature | Description |
|---------|-------------|
| **Versioning** | Every prompt change creates a new version; full history preserved |
| **Active/Inactive** | Only one version active per prompt; instant switch |
| **Rollback** | One-click rollback to any previous version |
| **Experiments** | A/B test two prompt versions; auto-select winner at significance |
| **Metrics** | Per-version: quality score, latency, cost, invocation count |
| **Template Variables** | Prompts use `{{variable}}` placeholders; validated at render time |
| **Dashboard UI** | View all prompts, versions, active experiments, metrics |

### Files

```
backend/promptops/
├── __init__.py
├── models.py                # PromptVersion, PromptExperiment
├── manager.py               # PromptManager — CRUD, activation, rollback
├── renderer.py              # PromptRenderer — template variable injection + validation
├── experimenter.py          # PromptExperimenter — A/B test lifecycle
├── metrics.py               # PromptMetrics — tracks per-version performance
└── migrator.py              # PromptMigrator — imports prompts from /prompts/*.md into DB

prompts/                     # Seed prompts (imported into PromptOps on first run)
├── resume_parser.md
├── match_scorer.md
├── resume_tailor.md
├── cover_letter.md
├── outreach_email.md
├── followup_email.md
├── qa_verification.md
└── daily_digest.md
```

---

## Enhancement 7: Chaos Testing Module

Intentionally injects failures to validate that fallback chains, retry logic, and graceful degradation work correctly.

### Failure Scenarios

| Scenario | What It Simulates | Expected Behavior |
|----------|-------------------|-------------------|
| `api_provider_down` | Gemini API returns 500 | Gateway falls back to Groq, then HuggingFace |
| `api_rate_limited` | Groq returns 429 | Rate limiter backs off; routes to next provider |
| `api_timeout` | HuggingFace hangs for 30s | Timeout → fallback → log degradation |
| `redis_outage` | Redis connection refused | Celery tasks queue in memory; alert in digest |
| `ats_form_change` | Greenhouse API returns 422 | Adapter retries with adjusted payload; flags for review |
| `email_auth_failure` | Gmail OAuth token expired | Refresh token flow; if fails, alert user |
| `all_ai_down` | All AI providers fail | Rule-based fallback; cached scores; manual mode |
| `job_source_blocked` | Adzuna returns 403 | Source cooldown; skip source; try alternatives |
| `full_chaos` | Random combination of above | System should continue operating in degraded mode |

### Design

```python
class ChaosModule:
    def enable_scenario(self, scenario_name: str, duration_seconds: int)
    def disable_scenario(self, scenario_name: str)
    def get_active_scenarios(self) -> list[ChaosScenario]
    def run_resilience_suite(self) -> ResilienceReport  # Runs all scenarios sequentially
```

### Files

```
backend/chaos/
├── __init__.py
├── module.py                # ChaosModule — scenario management
├── scenarios.py             # Predefined failure scenarios
├── interceptors.py          # Middleware that injects failures when scenarios active
├── reporter.py              # ResilienceReport — pass/fail per scenario + recovery time
└── config.yaml              # Scenario definitions (severity, duration, targets)

backend/api/
├── chaos.py                 # REST endpoints for dashboard chaos controls
```

> [!WARNING]
> Chaos testing is only enabled in development/staging. A `CHAOS_ENABLED=false` environment variable gates all chaos functionality in production.

---

## Enhancement 8: Plugin Architecture

Drop-in support for new job boards, AI providers, and outreach channels without modifying core code.

### Plugin Interface

```python
# Three plugin types — each extends a base interface
class BaseSourcePlugin(ABC):
    """Drop-in job board / source integration"""
    name: str
    def search_jobs(self, filters: JobFilters) -> list[JobListing]
    def get_job_details(self, job_id: str) -> JobListing
    def get_rate_limits(self) -> RateLimitConfig

class BaseProviderPlugin(ABC):
    """Drop-in AI provider"""
    name: str
    def generate(self, prompt: str, **kwargs) -> GenerationResult
    def embed(self, text: str) -> list[float]
    def get_capabilities(self) -> list[str]  # ["generate", "embed", "classify"]

class BaseChannelPlugin(ABC):
    """Drop-in outreach channel (email, LinkedIn DM, SMS, etc.)"""
    name: str
    def send_message(self, contact, message) -> SendResult
    def check_responses(self) -> list[InboundMessage]
    def get_delivery_status(self, message_id) -> DeliveryStatus

class BaseATSPlugin(BaseATSAdapter):
    """Drop-in ATS adapter (extends the adapter layer)"""
    pass
```

### Plugin Registration (config-driven)

```yaml
# config/plugins.yaml
plugins:
  sources:
    - name: "adzuna"
      module: "plugins.sources.adzuna"
      enabled: true
      priority: 1
    - name: "jsearch"
      module: "plugins.sources.jsearch"
      enabled: true
      priority: 2
    - name: "custom_company_feed"
      module: "plugins.sources.custom_rss"
      enabled: false
      config:
        feed_url: "https://example.com/jobs.rss"

  providers:
    - name: "gemini"
      module: "plugins.providers.gemini"
      enabled: true
    - name: "groq"
      module: "plugins.providers.groq"
      enabled: true

  channels:
    - name: "gmail"
      module: "plugins.channels.gmail"
      enabled: true
    - name: "linkedin_dm"
      module: "plugins.channels.linkedin_dm"
      enabled: false  # V2
```

### Files

```
backend/plugins/
├── __init__.py
├── base.py                  # BaseSourcePlugin, BaseProviderPlugin, BaseChannelPlugin
├── manager.py               # PluginManager — discovers, loads, validates plugins
├── registry.py              # PluginRegistry — runtime plugin lookup
├── validator.py             # PluginValidator — schema + health check on load
│
├── sources/                 # Built-in source plugins
│   ├── __init__.py
│   ├── adzuna.py
│   ├── jsearch.py
│   ├── remotive.py
│   └── custom_rss.py       # Generic RSS/Atom feed plugin
│
├── providers/               # Built-in AI provider plugins
│   ├── __init__.py
│   ├── gemini.py
│   ├── groq.py
│   ├── huggingface.py
│   ├── openrouter.py
│   ├── cerebras.py
│   ├── mistral.py
│   └── deepseek.py
│
└── channels/                # Built-in outreach channel plugins
    ├── __init__.py
    ├── gmail.py
    └── smtp_generic.py
```

**Key principle**: The core system never imports plugins directly. The `PluginManager` discovers them from config, validates they implement the correct interface, and registers them at runtime. New plugins = new file + YAML entry. Zero core code changes.

---

## Enhancement 9: Enhanced Mission Control Dashboard

The dashboard should feel like a **real operations center** — not just a CRUD app.

### Key Views

| View | Features |
|------|----------|
| **Mission Overview** | Real-time stats cards, agent health grid (green/yellow/red), live activity ticker, automation mode indicator, system uptime |
| **Agent Timeline** | Gantt-style timeline showing every agent's execution windows, task durations, and dependencies. Hover for details. |
| **Decision Trace** | For any application: "Why was this decision made?" — shows match score breakdown, which agent acted, which AI model was used, confidence factors, memory references |
| **Confidence Heatmap** | 2D heatmap: X = job sources, Y = time periods, color = average confidence score. Reveals which sources produce best matches |
| **Workflow Replay** | Select any application → replay the full agent workflow step-by-step: ingestion → matching → composition → submission. Each step shows inputs, outputs, AI calls, and timing |
| **Pipeline Kanban** | Drag-and-drop board: Discovered → Matched → Composing → Pending Review → Submitted → Acknowledged → Interview → Offer/Rejected |
| **Recruiter CRM** | Contact list with relationship scores, conversation threads, follow-up schedules, engagement charts |
| **PromptOps Console** | Prompt versions, active experiments, performance metrics, one-click rollback |
| **Evaluation Dashboard** | Match precision chart, callback rate trends, A/B test results, source effectiveness comparison |
| **Automation Mode Switcher** | Big toggle: Advisor ↔ Copilot ↔ Autopilot with clear explanation of what changes |
| **Chaos Console** | Enable/disable failure scenarios, run resilience suite, view pass/fail results (dev only) |
| **Settings** | AI API keys, job filters, schedules, digest preferences, plugin management |

### Dashboard Components

```
dashboard/src/components/
├── mission/
│   ├── MissionOverview.jsx      # Real-time stats + agent health grid
│   ├── AgentTimeline.jsx        # Gantt-style execution timeline
│   ├── ActivityTicker.jsx       # Live scrolling activity feed
│   └── SystemStatus.jsx         # Uptime, queue depth, AI provider status
│
├── intelligence/
│   ├── DecisionTrace.jsx        # "Why was this decision made?" viewer
│   ├── ConfidenceHeatmap.jsx    # 2D heatmap (source × time → confidence)
│   ├── WorkflowReplay.jsx       # Step-by-step workflow replay
│   └── MatchBreakdown.jsx       # Cosine sim + skill overlap + domain breakdown
│
├── pipeline/
│   ├── PipelineKanban.jsx       # Drag-and-drop application status board
│   ├── JobCard.jsx              # Individual job card with match score
│   ├── ApplicationDetail.jsx    # Full application detail + decision trace
│   └── ReviewQueue.jsx          # Items needing user attention
│
├── crm/
│   ├── RecruiterList.jsx        # Contact list with relationship scores
│   ├── ConversationThread.jsx   # Email thread viewer
│   ├── FollowUpCalendar.jsx     # Follow-up schedule calendar view
│   └── RelationshipChart.jsx    # Score trends over time
│
├── ops/
│   ├── PromptConsole.jsx        # PromptOps management UI
│   ├── EvalDashboard.jsx        # Evaluation metrics + A/B results
│   ├── ModeSwitcher.jsx         # Advisor ↔ Copilot ↔ Autopilot toggle
│   └── ChaosConsole.jsx         # Failure scenario controls
│
├── common/
│   ├── Layout.jsx
│   ├── Sidebar.jsx
│   ├── Header.jsx
│   ├── StatsCard.jsx
│   ├── Chart.jsx                # Reusable chart wrapper
│   └── SettingsPanel.jsx
│
└── pages/
    ├── Dashboard.jsx            # Mission Overview (default view)
    ├── Jobs.jsx                 # Job explorer + match heatmap
    ├── Applications.jsx         # Pipeline + workflow replay
    ├── CRM.jsx                  # Recruiter CRM
    ├── Analytics.jsx            # Eval dashboard + PromptOps
    ├── Operations.jsx           # Mode switcher + chaos console
    └── Settings.jsx             # Config management
```

---

## Complete Project Structure

```
k:/JOB/orbiter/
├── README.md
├── docker-compose.yml
├── Makefile
├── .env.example
│
├── config/
│   ├── default.yaml              # Global defaults
│   ├── ai_providers.yaml         # AI model config + fallback chains
│   ├── job_sources.yaml          # Job API source definitions
│   ├── automation_rules.yaml     # Modes + thresholds + approval rules
│   ├── schedules.yaml            # 24/7 cycle frequencies
│   ├── digest.yaml               # Daily digest config
│   ├── domain_taxonomy.yaml      # Skill-to-domain mappings
│   ├── ats_adapters.yaml         # ATS adapter registry
│   ├── plugins.yaml              # Plugin registration
│   ├── chaos_scenarios.yaml      # Chaos test definitions
│   └── templates/
│       ├── cover_letter_default.md
│       ├── recruiter_outreach.md
│       ├── follow_up.md
│       └── daily_digest.html
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── api/                      # REST API routes
│   │   ├── __init__.py
│   │   ├── profile.py
│   │   ├── jobs.py
│   │   ├── applications.py
│   │   ├── dashboard.py
│   │   ├── settings.py
│   │   ├── crm.py                # Recruiter CRM endpoints
│   │   ├── mode.py               # Automation mode endpoints
│   │   ├── promptops.py          # PromptOps endpoints
│   │   ├── evaluation.py         # Evaluation metrics endpoints
│   │   └── chaos.py              # Chaos testing endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # YAML config loader (hot-reload)
│   │   ├── database.py           # SQLAlchemy models + migrations
│   │   ├── events.py             # Redis event bus
│   │   ├── security.py           # Encryption + OAuth token management
│   │   ├── automation_mode.py    # Mode engine (Advisor/Copilot/Autopilot)
│   │   └── exceptions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── job.py
│   │   ├── match.py
│   │   ├── application.py
│   │   └── action_log.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py               # BaseAgent + BaseSupervisor
│   │   ├── master.py             # Master Orchestrator
│   │   ├── ingestion/            # Level 1A (A1-A4)
│   │   ├── intelligence/         # Level 1B (B1-B4)
│   │   ├── composition/          # Level 1C (C1-C4)
│   │   ├── execution/            # Level 1D (D1-D4)
│   │   └── reporting/            # Level 1E (E1-E3)
│   │
│   ├── adapters/                 # ATS Adapter Layer
│   │   ├── __init__.py
│   │   ├── base.py               # BaseATSAdapter
│   │   ├── registry.py           # Config-driven adapter lookup
│   │   ├── greenhouse.py
│   │   ├── lever.py
│   │   ├── ashby.py
│   │   ├── workday.py            # [V1]
│   │   └── generic_email.py
│   │
│   ├── plugins/                  # Plugin Architecture
│   │   ├── __init__.py
│   │   ├── base.py               # Plugin interfaces
│   │   ├── manager.py            # PluginManager
│   │   ├── registry.py           # Runtime registry
│   │   ├── validator.py
│   │   ├── sources/              # Built-in source plugins
│   │   ├── providers/            # Built-in AI provider plugins
│   │   └── channels/             # Built-in outreach channel plugins
│   │
│   ├── crm/                      # Recruiter CRM
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── service.py
│   │   ├── enrichment.py
│   │   ├── scoring.py
│   │   └── followup_engine.py
│   │
│   ├── memory/                   # Agent Memory
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── store.py
│   │   ├── patterns.py
│   │   ├── decay.py
│   │   └── feedback.py
│   │
│   ├── evaluation/               # Evaluation Framework
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tracker.py
│   │   ├── analyzer.py
│   │   ├── ab_testing.py
│   │   ├── reporter.py
│   │   └── feedback_loop.py
│   │
│   ├── promptops/                # PromptOps Subsystem
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── manager.py
│   │   ├── renderer.py
│   │   ├── experimenter.py
│   │   ├── metrics.py
│   │   └── migrator.py
│   │
│   ├── chaos/                    # Chaos Testing Module
│   │   ├── __init__.py
│   │   ├── module.py
│   │   ├── scenarios.py
│   │   ├── interceptors.py
│   │   └── reporter.py
│   │
│   ├── ai_gateway/               # AI Gateway (8 providers)
│   │   ├── __init__.py
│   │   ├── gateway.py
│   │   ├── rate_limiter.py
│   │   └── quality_check.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── profile_service.py
│   │   ├── job_service.py
│   │   ├── match_service.py
│   │   ├── compose_service.py
│   │   ├── apply_service.py
│   │   ├── email_service.py
│   │   ├── digest_service.py
│   │   └── analytics_service.py
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── schedules.py
│   │   ├── ingestion_tasks.py
│   │   ├── intelligence_tasks.py
│   │   ├── composition_tasks.py
│   │   ├── execution_tasks.py
│   │   ├── email_tasks.py
│   │   ├── digest_tasks.py
│   │   └── followup_tasks.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── dedup.py
│       ├── embedding.py
│       ├── pdf_parser.py
│       └── validators.py
│
├── dashboard/                    # React Mission Control Dashboard
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/
│       │   ├── mission/          # Mission Overview, Agent Timeline, Activity Ticker
│       │   ├── intelligence/     # Decision Trace, Confidence Heatmap, Workflow Replay
│       │   ├── pipeline/         # Kanban, Job Cards, Review Queue
│       │   ├── crm/              # Recruiter List, Conversations, Follow-ups
│       │   ├── ops/              # PromptOps, Eval Dashboard, Mode Switcher, Chaos
│       │   └── common/           # Layout, Sidebar, Header, StatsCard, Chart
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── Jobs.jsx
│       │   ├── Applications.jsx
│       │   ├── CRM.jsx
│       │   ├── Analytics.jsx
│       │   ├── Operations.jsx
│       │   └── Settings.jsx
│       ├── hooks/
│       └── utils/
│
├── prompts/                      # Seed prompts (imported to PromptOps)
│   ├── resume_parser.md
│   ├── match_scorer.md
│   ├── resume_tailor.md
│   ├── cover_letter.md
│   ├── outreach_email.md
│   ├── followup_email.md
│   ├── qa_verification.md
│   └── daily_digest.md
│
└── tests/
    ├── conftest.py
    ├── test_agents/
    ├── test_adapters/
    ├── test_plugins/
    ├── test_crm/
    ├── test_memory/
    ├── test_evaluation/
    ├── test_promptops/
    ├── test_chaos/
    ├── test_ai_gateway/
    ├── test_services/
    └── test_api/
```

---

## Revised MVP Build Order

### Phase 1: Foundation (Week 1-2)
- Project scaffolding + config system (YAML)
- Database models (all entities) + SQLite
- Plugin architecture (interfaces + manager + registry)
- AI Gateway with plugin-based providers (Gemini, Groq, HuggingFace, OpenRouter, etc.)
- Base agent framework + event bus + automation mode engine
- Gmail API OAuth setup

### Phase 2: Intelligence Core (Week 3-4)
- Resume parser agent (PDF → structured data + embeddings)
- Job ingestion via source plugins (Adzuna, JSearch, Remotive)
- Match engine (cosine similarity + skill overlap + domain fidelity)
- Classification agent + QA agent
- Agent memory store (initial — records decisions)
- PromptOps subsystem (versioning, rendering, seed prompt import)

### Phase 3: Composition + Execution (Week 5-6)
- Resume tailor agent + cover letter agent
- ATS adapter layer (Greenhouse, Lever, Ashby, generic email)
- Email apply agent (recruiter outreach via Gmail API)
- Tracking agent (status monitoring)
- Evaluation framework (tracker + basic metrics)

### Phase 4: CRM + 24/7 Operations (Week 7-8)
- Recruiter CRM (contacts, conversations, relationship scoring)
- Follow-up engine (72-hour automated follow-ups)
- Celery Beat schedules for all 24/7 cycles
- Email monitor agent (inbox parsing every 5 min)
- Daily digest agent (compile + send)
- Alert agent (urgent notifications)

### Phase 5: Mission Control Dashboard (Week 9-11)
- Core layout, navigation, dark mode design system
- Mission overview (stats, agent health, activity ticker)
- Pipeline kanban + review queue
- Agent timeline + decision trace viewer
- Confidence heatmap + workflow replay
- Recruiter CRM views
- PromptOps console + evaluation dashboard
- Automation mode switcher
- Settings management

### Phase 6: Hardening + Deploy (Week 12)
- Chaos testing module (all scenarios + resilience suite)
- A/B testing framework (evaluation + PromptOps experiments)
- Docker Compose for full stack
- Oracle Cloud deployment
- End-to-end 24-hour soak test
- Documentation

---

## Verification Plan

### Automated Tests
```bash
# Full test suite
cd k:/JOB/orbiter && python -m pytest tests/ -v --cov=backend

# Plugin validation
cd k:/JOB/orbiter && python -m pytest tests/test_plugins/ -v

# Chaos resilience suite
cd k:/JOB/orbiter && python -c "from backend.chaos.module import ChaosModule; ChaosModule().run_resilience_suite()"

# Dashboard build
cd k:/JOB/orbiter/dashboard && npm run build
```

### Manual Verification
1. Upload resume → verify parsing, embedding, memory storage
2. Trigger job discovery → verify source plugins return results
3. Switch automation modes → verify behavior changes per mode
4. Trigger auto-apply in Autopilot → verify ATS adapter submission
5. Check email monitoring → verify inbox parsing + CRM enrichment
6. Trigger daily digest → verify email content + formatting
7. Run chaos scenarios → verify fallback + recovery
8. Dashboard → verify all views: timeline, traces, heatmap, replay, CRM
9. 24-hour soak test → verify continuous 24/7 operation
