import logging
from celery import shared_task
from backend.agents.ingestion.api_source import api_source_agent

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_job_discovery(self):
    try:
        return api_source_agent.process({"type": "discover_jobs", "filters": {}})
    except Exception as e:
        logger.error(f"run_job_discovery failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
