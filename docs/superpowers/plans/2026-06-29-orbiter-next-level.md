# Orbiter Next-Level Enhancement Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform Orbiter from a functional prototype into a production-ready, intelligent, and professional job automation platform.

**Architecture:** Phased approach — Security foundation → Intelligence fixes → Dashboard overhaul → Production hardening. Each phase is independently deployable. Phase 1 runs 6 parallel agent tracks.

**Tech Stack:** Python/FastAPI, React/Vite, SQLAlchemy/Alembic, Celery/Redis, ChromaDB, Docker, JWT auth, Vitest

---

## Phase Overview

| Phase | Focus | Duration | Agents |
|-------|-------|----------|--------|
| **Phase 1** | Security & Reliability | Week 1-2 | 6 parallel tracks |
| **Phase 2** | Intelligence That Works | Week 3-4 | 4 parallel tracks |
| **Phase 3** | Professional Dashboard | Week 5-6 | 3 parallel tracks |
| **Phase 4** | Production Hardening | Week 7-8 | 3 parallel tracks |

---

## Phase 1: Security & Reliability (Parallel Execution)

### Track A: Backend Auth & Security
**Agent:** `security-agent`
**Files:**
- Create: `backend/core/auth.py`
- Create: `backend/api/deps.py`
- Modify: `backend/main.py` (CORS, middleware)
- Modify: `backend/api/*.py` (add auth dependency)
- Create: `tests/test_auth/test_auth.py`

### Track B: Database Migrations & Indexes
**Agent:** `database-agent`
**Files:**
- Create: `alembic.ini`
- Create: `alembic/env.py`
- Create: `alembic/versions/001_initial.py`
- Modify: `backend/models/*.py` (add indexes)
- Create: `tests/test_migrations/test_migrations.py`

### Track C: AI Gateway Hardening
**Agent:** `ai-gateway-agent`
**Files:**
- Modify: `backend/ai_gateway/gateway.py`
- Modify: `backend/ai_gateway/rate_limiter.py`
- Modify: `backend/ai_gateway/quality_check.py`
- Create: `backend/ai_gateway/retry.py`
- Create: `tests/test_ai_gateway/test_retry.py`

### Track D: Celery Task Hardening
**Agent:** `celery-agent`
**Files:**
- Modify: `backend/tasks/celery_app.py`
- Modify: `backend/tasks/*.py` (all task files)
- Create: `backend/tasks/error_handling.py`
- Create: `tests/test_tasks/test_error_handling.py`

### Track E: Infrastructure & Docker
**Agent:** `infra-agent`
**Files:**
- Create: `.gitignore`
- Create: `.dockerignore`
- Modify: `backend/Dockerfile`
- Modify: `docker-compose.yml`
- Create: `scripts/healthcheck.sh`

### Track F: Code Cleanup & Utilities
**Agent:** `cleanup-agent**
**Files:**
- Create: `backend/utils/json_parser.py`
- Modify: `backend/agents/intelligence/*.py` (use shared parser)
- Modify: `backend/main.py` (remove duplicate upload endpoint)
- Modify: `backend/agents/reporting/digest_agent.py` (use real DB data)
- Delete: `backend/tasks/schedules.py` (dead code)

---

## Phase 2: Intelligence That Works

### Track G: Real Tracking Agent
**Agent:** `tracking-agent`
**Files:**
- Modify: `backend/agents/execution/tracker.py`
- Create: `backend/services/tracking_service.py`
- Create: `tests/test_tracking/test_tracker.py`

### Track H: Statistical A/B Testing
**Agent:** `ab-testing-agent`
**Files:**
- Modify: `backend/evaluation/analyzer.py`
- Modify: `backend/evaluation/ab_testing.py`
- Create: `backend/evaluation/statistics.py`
- Create: `tests/test_evaluation/test_statistics.py`

### Track I: Working Chaos Testing
**Agent:** `chaos-agent`
**Files:**
- Modify: `backend/chaos/interceptors.py`
- Modify: `backend/chaos/module.py`
- Modify: `config/chaos_scenarios.yaml`
- Create: `tests/test_chaos/test_resilience.py`

### Track J: Effective Memory System
**Agent:** `memory-agent`
**Files:**
- Modify: `backend/memory/store.py`
- Modify: `backend/memory/decay.py`
- Modify: `backend/memory/patterns.py`
- Create: `tests/test_memory/test_effectiveness.py`

---

## Phase 3: Professional Dashboard

### Track K: Component Library
**Agent:** `ui-component-agent`
**Files:**
- Create: `dashboard/src/components/ui/Button.jsx`
- Create: `dashboard/src/components/ui/Card.jsx`
- Create: `dashboard/src/components/ui/Modal.jsx`
- Create: `dashboard/src/components/ui/Badge.jsx`
- Create: `dashboard/src/components/ui/Spinner.jsx`
- Create: `dashboard/src/components/ui/ErrorBanner.jsx`
- Create: `dashboard/src/components/ui/EmptyState.jsx`
- Create: `dashboard/src/styles/components.css`

### Track L: Responsive & Accessible
**Agent:** `a11y-agent`
**Files:**
- Modify: `dashboard/src/index.css` (media queries)
- Modify: `dashboard/src/components/common/Sidebar.jsx`
- Modify: `dashboard/src/pages/*.jsx` (aria labels, keyboard nav)
- Create: `dashboard/src/hooks/useKeyboard.js`

### Track M: Dashboard Modernization
**Agent:** `dashboard-agent`
**Files:**
- Modify: `dashboard/src/App.jsx` (code splitting)
- Modify: `dashboard/src/utils/api.js` (retry, AbortController)
- Delete: `dashboard/src/components/pipeline/PipelineKanban.jsx`
- Delete: `dashboard/src/App.css`
- Create: `dashboard/src/contexts/AppContext.jsx`

---

## Phase 4: Production Hardening

### Track N: TypeScript Migration
**Agent:** `typescript-agent`
**Files:**
- Create: `dashboard/tsconfig.json`
- Rename: `dashboard/src/**/*.{jsx,js}` → `*.{tsx,ts}`
- Create: `dashboard/src/types/index.ts`

### Track O: API & Component Tests
**Agent:** `testing-agent`
**Files:**
- Create: `dashboard/vitest.config.js`
- Create: `dashboard/src/**/*.test.{tsx,ts}`
- Modify: `tests/test_api/*.py` (add endpoint tests)

### Track P: Production Docker
**Agent:** `docker-agent`
**Files:**
- Modify: `backend/Dockerfile` (multi-stage, non-root)
- Modify: `docker-compose.yml` (health checks, resource limits)
- Create: `docker-compose.prod.yml`

---

## Agent Execution Order

```
Phase 1 (Parallel):
  ┌─ security-agent ─────────────┐
  ├─ database-agent ─────────────┤
  ├─ ai-gateway-agent ───────────┼──→ Phase 2 (Parallel):
  ├─ celery-agent ───────────────┤    ├─ tracking-agent
  ├─ infra-agent ────────────────┤    ├─ ab-testing-agent
  └─ cleanup-agent ──────────────┘    ├─ chaos-agent
                                      └─ memory-agent
                                           ↓
                                      Phase 3 (Parallel):
                                      ├─ ui-component-agent
                                      ├─ a11y-agent
                                      └─ dashboard-agent
                                           ↓
                                      Phase 4 (Parallel):
                                      ├─ typescript-agent
                                      ├─ testing-agent
                                      └─ docker-agent
```

---

## Success Criteria

### Phase 1
- [ ] All API endpoints require JWT auth
- [ ] CORS restricted to configured origins
- [ ] Alembic migrations run cleanly
- [ ] All foreign keys indexed
- [ ] AI gateway retries with exponential backoff
- [ ] Rate limiter uses Redis (works across workers)
- [ ] Celery tasks have retries and timeouts
- [ ] Docker runs as non-root
- [ ] `.gitignore` excludes secrets
- [ ] Dead code removed

### Phase 2
- [ ] Tracking agent polls real ATS status
- [ ] Digest agent queries actual DB data
- [ ] A/B tests report confidence intervals
- [ ] Chaos testing verifies gateway fallback
- [ ] Memory decay scales (no full table load)

### Phase 3
- [ ] Reusable component library (7+ components)
- [ ] Responsive on mobile/tablet/desktop
- [ ] Accessible (aria, keyboard nav, focus trapping)
- [ ] Route-based code splitting
- [ ] API calls use AbortController

### Phase 4
- [ ] Dashboard fully TypeScript
- [ ] 80%+ test coverage on critical paths
- [ ] Production Docker config with health checks
