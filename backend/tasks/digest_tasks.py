import logging
from celery import shared_task
from backend.agents.reporting.digest_agent import digest_agent

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_daily_digest(self):
    try:
        return digest_agent.process({"type": "generate_digest"})
    except Exception as e:
        logger.error(f"run_daily_digest failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
