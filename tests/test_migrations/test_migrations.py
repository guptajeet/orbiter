import pytest
import tempfile
import os
from sqlalchemy import create_engine, inspect
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
    
    engine = None
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
        
        inspector = inspect(engine)
        actual_tables = inspector.get_table_names()
        
        for table in expected_tables:
            assert table in actual_tables, f"Table {table} not found after migration"
        
    finally:
        if engine:
            engine.dispose()
        os.unlink(tmp_path)


def test_indexes_created():
    """Test that indexes are created correctly."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        tmp_path = tmp.name
    
    engine = None
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{tmp_path}")
        
        command.upgrade(alembic_cfg, "head")
        
        engine = create_engine(f"sqlite:///{tmp_path}")
        inspector = inspect(engine)
        
        # Check indexes on applications table
        indexes = inspector.get_indexes('applications')
        index_names = [idx['name'] for idx in indexes]
        
        assert 'ix_applications_user_id' in index_names
        assert 'ix_applications_status' in index_names
        
    finally:
        if engine:
            engine.dispose()
        os.unlink(tmp_path)