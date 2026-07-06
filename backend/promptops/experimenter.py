import uuid
import random
from backend.core.database import SessionLocal
from backend.promptops.models import PromptExperiment

class PromptExperimenter:
    def start_experiment(self, prompt_name: str, control_id: str, treatment_id: str, metric: str):
        db = SessionLocal()
        try:
            exp = PromptExperiment(
                id=str(uuid.uuid4()),
                prompt_name=prompt_name,
                control_version_id=control_id,
                treatment_version_id=treatment_id,
                metric=metric,
                status="running"
            )
            db.add(exp)
            db.commit()
            return exp.id
        finally:
            db.close()

    def get_variant_for_request(self, prompt_name: str) -> str:
        """Returns the version ID to use based on traffic split"""
        db = SessionLocal()
        try:
            exp = db.query(PromptExperiment).filter(
                PromptExperiment.prompt_name == prompt_name,
                PromptExperiment.status == "running"
            ).first()
            
            if not exp:
                # Fallback to active version if no experiment
                from .manager import prompt_manager
                active = prompt_manager.get_active_prompt(prompt_name)
                return active.id if active else None
                
            # Randomly select variant based on traffic split (e.g., 50/50)
            if random.random() < exp.traffic_split.get("control", 0.5):
                return exp.control_version_id
            else:
                return exp.treatment_version_id
        finally:
            db.close()

prompt_experimenter = PromptExperimenter()
