import uuid
from backend.core.database import SessionLocal
from backend.promptops.models import PromptVersion

class PromptManager:
    def get_active_prompt(self, prompt_name: str) -> PromptVersion:
        db = SessionLocal()
        try:
            return db.query(PromptVersion).filter(
                PromptVersion.prompt_name == prompt_name,
                PromptVersion.is_active == True
            ).first()
        finally:
            db.close()

    def create_version(self, prompt_name: str, content: str, variables: list, author: str) -> str:
        db = SessionLocal()
        try:
            # Get latest version number
            latest = db.query(PromptVersion).filter(
                PromptVersion.prompt_name == prompt_name
            ).order_by(PromptVersion.version.desc()).first()
            
            version_num = latest.version + 1 if latest else 1
            
            pv = PromptVersion(
                id=str(uuid.uuid4()),
                prompt_name=prompt_name,
                version=version_num,
                content=content,
                variables=variables,
                author=author,
                is_active=False
            )
            db.add(pv)
            db.commit()
            return pv.id
        finally:
            db.close()

    def activate_version(self, prompt_name: str, version_id: str):
        db = SessionLocal()
        try:
            # Deactivate all
            db.query(PromptVersion).filter(
                PromptVersion.prompt_name == prompt_name
            ).update({"is_active": False})
            
            # Activate specific
            db.query(PromptVersion).filter(
                PromptVersion.id == version_id
            ).update({"is_active": True})
            
            db.commit()
        finally:
            db.close()

prompt_manager = PromptManager()
