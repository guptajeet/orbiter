"""initial tables

Revision ID: 001
Revises: 
Create Date: 2026-06-29 00:23:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email_accounts', sa.JSON(), nullable=True),
        sa.Column('linkedin_url', sa.String(), nullable=True),
        sa.Column('indeed_url', sa.String(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('automation_config', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create resume_profiles table
    op.create_table(
        'resume_profiles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('label', sa.String(), nullable=True),
        sa.Column('raw_text', sa.String(), nullable=True),
        sa.Column('parsed_sections', sa.JSON(), nullable=True),
        sa.Column('domain_tags', sa.JSON(), nullable=True),
        sa.Column('industry_tags', sa.JSON(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user_profiles.id'])
    )

    # Create job_listings table
    op.create_table(
        'job_listings',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('source_type', sa.String(), nullable=True),
        sa.Column('source_name', sa.String(), nullable=True),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('company_name', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('salary_range', sa.String(), nullable=True),
        sa.Column('description_raw', sa.String(), nullable=True),
        sa.Column('description_clean', sa.String(), nullable=True),
        sa.Column('domain_tags', sa.JSON(), nullable=True),
        sa.Column('industry_tags', sa.JSON(), nullable=True),
        sa.Column('required_skills', sa.JSON(), nullable=True),
        sa.Column('first_seen_at', sa.DateTime(), nullable=True),
        sa.Column('last_refreshed_at', sa.DateTime(), nullable=True),
        sa.Column('dedup_hash', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dedup_hash')
    )

    # Create match_results table
    op.create_table(
        'match_results',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('resume_id', sa.String(), nullable=True),
        sa.Column('job_id', sa.String(), nullable=True),
        sa.Column('cosine_similarity', sa.Float(), nullable=True),
        sa.Column('domain_fidelity_score', sa.Float(), nullable=True),
        sa.Column('skill_overlap_pct', sa.Float(), nullable=True),
        sa.Column('confidence_tier', sa.String(), nullable=True),
        sa.Column('scenario_classification', sa.String(), nullable=True),
        sa.Column('tailoring_suggestions', sa.JSON(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['resume_id'], ['resume_profiles.id']),
        sa.ForeignKeyConstraint(['job_id'], ['job_listings.id'])
    )

    # Create applications table
    op.create_table(
        'applications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('match_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('submission_method', sa.String(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('status_updated_at', sa.DateTime(), nullable=True),
        sa.Column('tailored_resume_snapshot', sa.String(), nullable=True),
        sa.Column('cover_letter_snapshot', sa.String(), nullable=True),
        sa.Column('tracking_events', sa.JSON(), nullable=True),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['match_id'], ['match_results.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user_profiles.id'])
    )

    # Create action_logs table
    op.create_table(
        'action_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('agent_id', sa.String(), nullable=True),
        sa.Column('action_type', sa.String(), nullable=True),
        sa.Column('input_summary', sa.String(), nullable=True),
        sa.Column('output_summary', sa.String(), nullable=True),
        sa.Column('model_used', sa.String(), nullable=True),
        sa.Column('model_provider', sa.String(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('duration_ms', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recruiter_contacts table
    op.create_table(
        'recruiter_contacts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('linkedin_url', sa.String(), nullable=True),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('department', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('relationship_score', sa.Float(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('first_contact_at', sa.DateTime(), nullable=True),
        sa.Column('last_interaction_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create crm_conversations table
    op.create_table(
        'crm_conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('contact_id', sa.String(), nullable=True),
        sa.Column('application_id', sa.String(), nullable=True),
        sa.Column('thread_id', sa.String(), nullable=True),
        sa.Column('messages', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('next_followup_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['contact_id'], ['recruiter_contacts.id']),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'])
    )

    # Create followup_schedules table
    op.create_table(
        'followup_schedules',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=True),
        sa.Column('contact_id', sa.String(), nullable=True),
        sa.Column('trigger_type', sa.String(), nullable=True),
        sa.Column('interval_hours', sa.Integer(), nullable=True),
        sa.Column('max_followups', sa.Integer(), nullable=True),
        sa.Column('current_count', sa.Integer(), nullable=True),
        sa.Column('last_sent_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['crm_conversations.id']),
        sa.ForeignKeyConstraint(['contact_id'], ['recruiter_contacts.id'])
    )

    # Create agent_memories table
    op.create_table(
        'agent_memories',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('agent_id', sa.String(), nullable=True),
        sa.Column('memory_type', sa.String(), nullable=True),
        sa.Column('content', sa.JSON(), nullable=True),
        sa.Column('relevance_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_accessed_at', sa.DateTime(), nullable=True),
        sa.Column('access_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create evaluation_metrics table
    op.create_table(
        'evaluation_metrics',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('context', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create experiment_results table
    op.create_table(
        'experiment_results',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('experiment_id', sa.String(), nullable=True),
        sa.Column('variant_name', sa.String(), nullable=True),
        sa.Column('outcome_value', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create prompt_versions table
    op.create_table(
        'prompt_versions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('prompt_name', sa.String(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('variables', sa.JSON(), nullable=True),
        sa.Column('author', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('performance_metrics', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create prompt_experiments table
    op.create_table(
        'prompt_experiments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('prompt_name', sa.String(), nullable=True),
        sa.Column('control_version_id', sa.String(), nullable=True),
        sa.Column('treatment_version_id', sa.String(), nullable=True),
        sa.Column('traffic_split', sa.JSON(), nullable=True),
        sa.Column('metric', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('results', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['control_version_id'], ['prompt_versions.id']),
        sa.ForeignKeyConstraint(['treatment_version_id'], ['prompt_versions.id'])
    )

    # Add indexes for foreign keys and common queries
    op.create_index('ix_user_profiles_email', 'user_profiles', ['email_accounts'])
    op.create_index('ix_resume_profiles_user_id', 'resume_profiles', ['user_id'])
    op.create_index('ix_job_listings_dedup_hash', 'job_listings', ['dedup_hash'])
    op.create_index('ix_match_results_resume_id', 'match_results', ['resume_id'])
    op.create_index('ix_match_results_job_id', 'match_results', ['job_id'])
    op.create_index('ix_applications_match_id', 'applications', ['match_id'])
    op.create_index('ix_applications_user_id', 'applications', ['user_id'])
    op.create_index('ix_applications_status', 'applications', ['status'])
    op.create_index('ix_action_logs_agent_id', 'action_logs', ['agent_id'])
    op.create_index('ix_action_logs_created_at', 'action_logs', ['created_at'])
    op.create_index('ix_recruiter_contacts_email', 'recruiter_contacts', ['email'])
    op.create_index('ix_crm_conversations_contact_id', 'crm_conversations', ['contact_id'])
    op.create_index('ix_evaluation_metrics_metric_name', 'evaluation_metrics', ['metric_name'])


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
    op.drop_index('ix_job_listings_dedup_hash', table_name='job_listings')
    op.drop_index('ix_resume_profiles_user_id', table_name='resume_profiles')
    op.drop_index('ix_user_profiles_email', table_name='user_profiles')

    # Drop tables in reverse order of creation
    op.drop_table('prompt_experiments')
    op.drop_table('prompt_versions')
    op.drop_table('experiment_results')
    op.drop_table('evaluation_metrics')
    op.drop_table('agent_memories')
    op.drop_table('followup_schedules')
    op.drop_table('crm_conversations')
    op.drop_table('recruiter_contacts')
    op.drop_table('action_logs')
    op.drop_table('applications')
    op.drop_table('match_results')
    op.drop_table('job_listings')
    op.drop_table('resume_profiles')
    op.drop_table('user_profiles')