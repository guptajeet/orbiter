import uuid
from backend.core.database import SessionLocal
from backend.models.user import UserProfile
from backend.models.resume import ResumeProfile

class ProfileService:
    def get_or_create_default(self) -> UserProfile:
        db = SessionLocal()
        try:
            profile = db.query(UserProfile).filter(UserProfile.id == "default_user").first()
            if not profile:
                profile = UserProfile(id="default_user", preferences={})
                db.add(profile)
                db.commit()
            return profile
        finally:
            db.close()
    
    def get_resumes(self, user_id: str = "default_user") -> list:
        db = SessionLocal()
        try:
            return db.query(ResumeProfile).filter(ResumeProfile.user_id == user_id).all()
        finally:
            db.close()
    
    def update_preferences(self, preferences: dict, user_id: str = "default_user"):
        db = SessionLocal()
        try:
            profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
            if profile:
                profile.preferences = {**(profile.preferences or {}), **preferences}
                db.commit()
            return profile
        finally:
            db.close()

profile_service = ProfileService()
