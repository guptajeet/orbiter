# Alembic Migrations and Database Indexes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Alembic migrations and database indexes to the Orbiter backend for proper schema management and query optimization.

**Architecture:** Integrate Alembic for database migration support, replacing the current `create_all()` approach. Add indexes on foreign key columns and composite indexes for common queries.

**Tech Stack:** Alembic, SQLAlchemy, SQLite

---

## Task 1: Add alembic to requirements.txt

**Files:**
- Modify: `backend/requirements.txt`

- [ ] **Step 1: Add alembic dependency**

```python
# Add to the end of the file
alembic>=1.13.0
```

- [ ] **Step 2: Install dependencies**

Run: `cd K:\JOB\orbiter && pip install -r backend/requirements.txt`
Expected: alembic installed successfully

- [ ] **Step 3: Commit**

```bash
git add backend/requirements.txt
git commit -m "feat: add alembic dependency for database migrations"
```

---

## Task 2: Create alembic.ini configuration

**Files:**
- Create: `alembic.ini`

- [ ] **Step 1: Create alembic.ini file**

```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///./orbiter.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

- [ ] **Step 2: Commit**

```bash
git add alembic.ini
git commit -m "feat: create alembic configuration file"
```

---

## Task 3: Create alembic directory structure and env.py

**Files:**
- Create: `alembic/env.py`
- Create: `alembic/script.py.mako`

- [ ] **Step 1: Create alembic directory**

Run: `mkdir -p alembic/versions`

- [ ] **Step 2: Create alembic/env.py**

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.models.base import Base
from backend.core.config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all models so Alembic sees them
from backend.models import user, resume, job, match, application, action_log
from backend.crm.models import RecruiterContact, Conversation, FollowUpSchedule
from backend.memory.models import AgentMemory
from backend.evaluation.models import EvaluationMetric, ExperimentResult
from backend.promptops.models import PromptVersion, PromptExperiment

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: Create alembic/script.py.mako**

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> ${upgrades if upgrades else "pass"}:
    ${upgrades if upgrades else "pass"}


def downgrade() -> ${downgrades if downgrades else "pass"}:
    ${downgrades if downgrades else "pass"}
```

- [ ] **Step 4: Commit**

```bash
git add alembic/
git commit -m "feat: create alembic directory structure and environment"
```

---

## Task 4: Generate initial migration with indexes

**Files:**
- Create: `alembic/versions/001_initial.py`

- [ ] **Step 1: Generate initial migration**

Run: `cd K:\JOB\orbiter && python -m alembic revision --autogenerate -m "initial tables"`
Expected: Migration file created in alembic/versions/

- [ ] **Step 2: Edit migration to add indexes**

Open the generated migration file and add the following indexes to the upgrade() function:

```python
# Add these indexes after the create_all operations
op.create_index('ix_users_email', 'user_profiles', ['email'])
op.create_index('ix_resume_profiles_user_id', 'resume_profiles', ['user_id'])
op.create_index('ix_jobs_dedup_hash', 'job_listings', ['dedup_hash'])
op.create_index('ix_match_score_resume_id', 'match_results', ['resume_id'])
op.create_index('ix_match_score_job_id', 'match_results', ['job_id'])
op.create_index('ix_applications_match_id', 'applications', ['match_id'])
op.create_index('ix_applications_user_id', 'applications', ['user_id'])
op.create_index('ix_applications_status', 'applications', ['status'])
op.create_index('ix_action_log_agent_id', 'action_logs', ['agent_id'])
op.create_index('ix_action_log_created_at', 'action_logs', ['created_at'])
op.create_index('ix_crm_contacts_user_id', 'recruiter_contacts', ['email'])
op.create_index('ix_crm_conversations_contact_id', 'crm_conversations', ['contact_id'])
op.create_index('ix_evaluation_metrics_name', 'evaluation_metrics', ['metric_name'])
```

- [ ] **Step 3: Commit**

```bash
git add alembic/versions/
git commit -m "feat: add initial migration with database indexes"
```

---

## Task 5: Modify main.py to use Alembic

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: Update main.py to use Alembic**

Replace line 32 (`Base.metadata.create_all(bind=engine)`) with:

```python
# Keep create_all as fallback for fresh installs, but prefer migrations
from alembic.config import Config
from alembic import command
try:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
except Exception:
    Base.metadata.create_all(bind=engine)
```

- [ ] **Step 2: Commit**

```bash
git add backend/main.py
git commit -m "feat: integrate alembic migrations into application startup"
```

---

## Task 6: Create migration tests

**Files:**
- Create: `tests/test_migrations/__init__.py`
- Create: `tests/test_migrations/test_migrations.py`

- [ ] **Step 1: Create test directory**

Run: `mkdir -p tests/test_migrations`

- [ ] **Step 2: Create test file**

```python
import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from backend.models.base import Base
from backend.models.user import UserProfile
from backend.models.resume import ResumeProfile
from backend.models.job import JobListing
from backend.models.match import MatchResult
from backend.models.application import Application
from backend.models.action_log import ActionLog
from backend.crm.models import RecruiterContact, Conversation, FollowUpSchedule
from backend.memory.models import AgentMemory
from backend.evaluation.models import EvaluationMetric, ExperimentResult
from backend.promptops.models import PromptVersion, PromptExperiment


def test_alembic_migration_runs_cleanly():
    """Test that alembic upgrade head runs without errors on a fresh database."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Create a temporary alembic config
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{tmp_path}")
        
        # Run migration
        command.upgrade(alembic_cfg, "head")
        
        # Verify tables exist
        engine = create_engine(f"sqlite:///{tmp_path}")
        Base.metadata.bind = engine
        
        expected_tables = [
            'user_profiles', 'resume_profiles', 'job_listings', 
            'match_results', 'applications', 'action_logs',
            'recruiter_contacts', 'crm_conversations', 'followup_schedules',
            'agent_memories', 'evaluation_metrics', 'experiment_results',
            'prompt_versions', 'prompt_experiments'
        ]
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        actual_tables = inspector.get_table_names()
        
        for table in expected_tables:
            assert table in actual_tables, f"Table {table} not found after migration"
        
    finally:
        os.unlink(tmp_path)


def test_indexes_created():
    """Test that indexes are created correctly."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{tmp_path}")
        
        command.upgrade(alembic_cfg, "head")
        
        engine = create_engine(f"sqlite:///{tmp_path}")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        # Check indexes on applications table
        indexes = inspector.get_indexes('applications')
        index_names = [idx['name'] for idx in indexes]
        
        assert 'ix_applications_user_id' in index_names
        assert 'ix_applications_status' in index_names
        
    finally:
        os.unlink(tmp_path)
```

- [ ] **Step 3: Run tests**

Run: `cd K:\JOB\orbiter && python -m pytest tests/test_migrations/test_migrations.py -v`
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add tests/test_migrations/
git commit -m "feat: add migration tests"
```

---

## Task 7: Verify complete integration

**Files:**
- None (verification only)

- [ ] **Step 1: Run all tests**

Run: `cd K:\JOB\orbiter && python -m pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 2: Test application startup**

Run: `cd K:\JOB\orbiter && python -c "from backend.main import app; print('App imports successfully')"`
Expected: No import errors

- [ ] **Step 3: Final commit**

```bash
git add .
git commit -m "feat: complete alembic migration integration with indexes"
```

---

## Summary

**Files Created:**
- `alembic.ini` - Alembic configuration
- `alembic/env.py` - Alembic environment setup
- `alembic/script.py.mako` - Migration template
- `alembic/versions/001_initial.py` - Initial migration with indexes
- `tests/test_migrations/__init__.py` - Test package init
- `tests/test_migrations/test_migrations.py` - Migration tests

**Files Modified:**
- `backend/requirements.txt` - Added alembic dependency
- `backend/main.py` - Integrated Alembic into startup

**Indexes Added:**
- `ix_users_email` on user_profiles
- `ix_resume_profiles_user_id` on resume_profiles
- `ix_jobs_dedup_hash` on job_listings
- `ix_match_score_resume_id` on match_results
- `ix_match_score_job_id` on match_results
- `ix_applications_match_id` on applications
- `ix_applications_user_id` on applications
- `ix_applications_status` on applications
- `ix_action_log_agent_id` on action_logs
- `ix_action_log_created_at` on action_logs
- `ix_crm_contacts_user_id` on recruiter_contacts
- `ix_crm_conversations_contact_id` on crm_conversations
- `ix_evaluation_metrics_name` on evaluation_metrics
