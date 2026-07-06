import logging
from celery import shared_task
from backend.agents.ingestion.email_monitor import email_monitor_agent

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_email_monitor(self):
    try:
        return email_monitor_agent.process({"type": "check_inbox"})
    except Exception as e:
        logger.error(f"run_email_monitor failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
