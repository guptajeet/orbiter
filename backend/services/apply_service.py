import uuid
from backend.core.database import SessionLocal
from backend.models.application import Application
from backend.adapters.registry import adapter_registry

class ApplyService:
    def submit_application(self, application_id: str, method: str = "api"):
        db = SessionLocal()
        try:
            app = db.query(Application).filter(Application.id == application_id).first()
            if not app:
                return {"status": "error", "message": "Application not found"}
            
            app.status = "submitted"
            app.submission_method = method
            db.commit()
            return {"status": "success", "application_id": application_id}
        finally:
            db.close()
    
    def get_application_count(self, status: str = None) -> int:
        db = SessionLocal()
        try:
            query = db.query(Application)
            if status:
                query = query.filter(Application.status == status)
            return query.count()
        finally:
            db.close()

apply_service = ApplyService()
