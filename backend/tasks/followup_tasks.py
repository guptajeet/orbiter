import logging
from celery import shared_task
from backend.crm.followup_engine import followup_engine

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_followup_check(self):
    try:
        followup_engine.process_due_followups()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"run_followup_check failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
