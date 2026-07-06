import os
import logging
import uvicorn
from dotenv import load_dotenv

# Load .env BEFORE anything else imports settings
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.database import engine
from backend.models import Base
from backend.api.profile import router as profile_router
from backend.api.jobs import router as jobs_router
from backend.api.applications import router as applications_router
from backend.api.dashboard import router as dashboard_router
from backend.api.settings import router as settings_router
from backend.api.crm import router as crm_router
from backend.api.mode import router as mode_router
from backend.api.promptops import router as promptops_router
from backend.api.evaluation import router as evaluation_router
from backend.api.chaos import router as chaos_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DB tables - prefer Alembic migrations, fallback to create_all
from alembic.config import Config
from alembic import command
try:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
except Exception as e:
    logger.warning(f"Alembic migration failed, falling back to create_all: {e}")
    Base.metadata.create_all(bind=engine)

# Load plugins
try:
    from backend.plugins.manager import plugin_manager
    plugin_manager.load_plugins()
    from backend.plugins.registry import registry
    logger.info(f"Plugins loaded. Providers: {list(registry.providers.keys())}")
except Exception as e:
    logger.warning(f"Plugin loading failed: {e}")

# Seed prompts into DB
from backend.promptops.migrator import prompt_migrator
try:
    prompt_migrator.migrate_from_files()
except Exception as e:
    logger.warning(f"Startup prompt migration failed: {e}")

# Wire up master orchestrator with supervisors
from backend.agents.master import master

try:
    from backend.agents.ingestion import ingestion_supervisor
    master.register_supervisor("ingestion", ingestion_supervisor)
except Exception as e:
    logger.warning(f"Failed to load ingestion supervisor: {e}")

try:
    from backend.agents.intelligence import intelligence_supervisor
    master.register_supervisor("intelligence", intelligence_supervisor)
except Exception as e:
    logger.warning(f"Failed to load intelligence supervisor: {e}")

try:
    from backend.agents.composition import composition_supervisor
    master.register_supervisor("composition", composition_supervisor)
except Exception as e:
    logger.warning(f"Failed to load composition supervisor: {e}")

try:
    from backend.agents.execution import execution_supervisor
    master.register_supervisor("execution", execution_supervisor)
except Exception as e:
    logger.warning(f"Failed to load execution supervisor: {e}")

try:
    from backend.agents.reporting import reporting_supervisor
    master.register_supervisor("reporting", reporting_supervisor)
except Exception as e:
    logger.warning(f"Failed to load reporting supervisor: {e}")

logger.info("Pipeline wired: master orchestrator connected to supervisors")

app = FastAPI(title="Orbiter Mission Control API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(dashboard_router)
app.include_router(settings_router)
app.include_router(crm_router)
app.include_router(mode_router)
app.include_router(promptops_router)
app.include_router(evaluation_router)
app.include_router(chaos_router)

@app.get("/api/health")
def health_check():
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
