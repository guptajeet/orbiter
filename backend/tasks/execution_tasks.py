import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_application_submission(self, application_id: str):
    from backend.agents.execution.api_apply import api_apply_agent
    try:
        return api_apply_agent.process({
            "type": "submit_application",
            "application_id": application_id,
        })
    except Exception as e:
        logger.error(f"run_application_submission failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_status_tracking(self, application_id: str):
    from backend.agents.execution.tracker import tracking_agent
    try:
        return tracking_agent.process({
            "type": "track_application",
            "application_id": application_id,
        })
    except Exception as e:
        logger.error(f"run_status_tracking failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_email_outreach(self, contact_id: str, message: str):
    from backend.agents.execution.email_apply import email_apply_agent
    try:
        return email_apply_agent.process({
            "type": "email_application",
            "contact": {"id": contact_id},
            "message": {"body": message},
        })
    except Exception as e:
        logger.error(f"run_email_outreach failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
