"""add indexes

Revision ID: 002
Revises: 001
Create Date: 2026-06-29 00:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add indexes for foreign keys and common queries
    # Use IF NOT EXISTS to handle cases where indexes already exist from create_all()
    op.execute("CREATE INDEX IF NOT EXISTS ix_match_results_resume_id ON match_results (resume_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_match_results_job_id ON match_results (job_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_applications_match_id ON applications (match_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_applications_user_id ON applications (user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_applications_status ON applications (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_action_logs_agent_id ON action_logs (agent_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_action_logs_created_at ON action_logs (created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_recruiter_contacts_email ON recruiter_contacts (email)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_crm_conversations_contact_id ON crm_conversations (contact_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_evaluation_metrics_metric_name ON evaluation_metrics (metric_name)")


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_evaluation_metrics_metric_name', table_name='evaluation_metrics')
    op.drop_index('ix_crm_conversations_contact_id', table_name='crm_conversations')
    op.drop_index('ix_recruiter_contacts_email', table_name='recruiter_contacts')
    op.drop_index('ix_action_logs_created_at', table_name='action_logs')
    op.drop_index('ix_action_logs_agent_id', table_name='action_logs')
    op.drop_index('ix_applications_status', table_name='applications')
    op.drop_index('ix_applications_user_id', table_name='applications')
    op.drop_index('ix_applications_match_id', table_name='applications')
    op.drop_index('ix_match_results_job_id', table_name='match_results')
    op.drop_index('ix_match_results_resume_id', table_name='match_results')