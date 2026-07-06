from dotenv import load_dotenv
# Load .env BEFORE anything else imports settings
load_dotenv(override=True)

from celery import Celery
from backend.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Load plugins so that Celery worker subprocesses have registry populated
try:
    from backend.plugins.manager import plugin_manager
    plugin_manager.load_plugins()
    from backend.plugins.registry import registry
    logger.info(f"Plugins loaded in Celery. Providers: {list(registry.providers.keys())}")
except Exception as e:
    logger.warning(f"Plugin loading failed in Celery: {e}")

redis_url = settings.default_config.get("system", {}).get("redis_url", "redis://localhost:6379/0")

celery_app = Celery("orbiter_tasks", broker=redis_url, backend=redis_url)

celery_app.conf.imports = (
    "backend.tasks.ingestion_tasks",
    "backend.tasks.intelligence_tasks",
    "backend.tasks.composition_tasks",
    "backend.tasks.execution_tasks",
    "backend.tasks.email_tasks",
    "backend.tasks.followup_tasks",
    "backend.tasks.digest_tasks",
)

# Load schedules from config
schedules_config = settings.schedules.get("schedules", {})

celery_app.conf.beat_schedule = {
    "job_discovery": {
        "task": "backend.tasks.ingestion_tasks.run_job_discovery",
        "schedule": float(schedules_config.get("job_discovery", 7200.0)),
    },
    "email_monitoring": {
        "task": "backend.tasks.email_tasks.run_email_monitor",
        "schedule": float(schedules_config.get("email_monitoring", 300.0)),
    },
    "followup_check": {
        "task": "backend.tasks.followup_tasks.run_followup_check",
        "schedule": float(schedules_config.get("followup_check", 3600.0)),
    },
    "daily_digest": {
        "task": "backend.tasks.digest_tasks.run_daily_digest",
        "schedule": float(schedules_config.get("daily_digest", 86400.0)),
    }
}
celery_app.conf.timezone = 'UTC'

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_soft_time_limit=120,
    task_time_limit=180,
    task_default_retry_delay=60,
    task_max_retries=3,
    task_default_queue='default',
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def test_task(self):
    logger.info("Celery test task executed")
    return "success"
