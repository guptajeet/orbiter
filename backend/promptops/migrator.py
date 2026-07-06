import os
from .manager import prompt_manager
from backend.core.config import settings

class PromptMigrator:
    def migrate_from_files(self):
        """Imports prompts from /prompts directory into DB"""
        prompts_dir = settings.default_config.get("paths", {}).get("prompts_dir", "../prompts")
        if not os.path.exists(prompts_dir):
            for cand in ["prompts", "backend/prompts", "../prompts", "../../prompts"]:
                if os.path.exists(cand):
                    prompts_dir = cand
                    break
        if not os.path.exists(prompts_dir):
            return
            
        for filename in os.listdir(prompts_dir):
            if filename.endswith(".md"):
                prompt_name = filename.replace(".md", "")
                filepath = os.path.join(prompts_dir, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                    
                # Check if this exact prompt version content already exists
                from backend.core.database import SessionLocal
                from backend.promptops.models import PromptVersion
                db = SessionLocal()
                try:
                    existing = db.query(PromptVersion).filter(
                        PromptVersion.prompt_name == prompt_name,
                        PromptVersion.content == content
                    ).first()
                    if existing:
                        if not existing.is_active:
                            prompt_manager.activate_version(prompt_name, existing.id)
                        continue
                finally:
                    db.close()

                # Simple variable extraction logic
                import re
                variables = list(set(re.findall(r"\{\{([^}]+)\}\}", content)))
                
                version_id = prompt_manager.create_version(prompt_name, content, variables, "system")
                prompt_manager.activate_version(prompt_name, version_id)
                print(f"Migrated prompt: {prompt_name}")

prompt_migrator = PromptMigrator()
