import uuid
from backend.core.database import SessionLocal
from backend.models.application import Application

class ComposeService:
    def get_pending_review(self):
        db = SessionLocal()
        try:
            return db.query(Application).filter(
                Application.status == "pending_approval"
            ).all()
        finally:
            db.close()
    
    def approve_application(self, app_id: str):
        db = SessionLocal()
        try:
            app = db.query(Application).filter(Application.id == app_id).first()
            if app:
                app.status = "submitted"
                db.commit()
            return app
        finally:
            db.close()
    
    def reject_application(self, app_id: str):
        db = SessionLocal()
        try:
            app = db.query(Application).filter(Application.id == app_id).first()
            if app:
                app.status = "rejected"
                db.commit()
            return app
        finally:
            db.close()

compose_service = ComposeService()
