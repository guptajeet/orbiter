import logging
import datetime
from backend.agents.base import BaseAgent
from backend.services.email_service import email_service
from backend.core.database import SessionLocal
from backend.models.job import JobListing
from backend.models.match import MatchResult
from backend.models.application import Application

logger = logging.getLogger(__name__)

class DigestAgent(BaseAgent):
    def __init__(self):
        super().__init__("digest_agent")

    def process(self, task: dict):
        if task.get("type") != "generate_digest":
            return {"status": "ignored"}
            
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        db = SessionLocal()
        try:
            total_jobs = db.query(JobListing).count()
            total_matches = db.query(MatchResult).count()
            high_matches = db.query(MatchResult).filter(MatchResult.cosine_similarity >= 0.8).count()
            pending_apps = db.query(Application).filter(Application.status == "pending_approval").count()
            submitted_apps = db.query(Application).filter(Application.status == "submitted").count()
            
            html_body = f"""
            <html>
                <body>
                    <h2>Orbiter Daily Mission Report ({today})</h2>
                    <p>System running autonomously. Here is your summary:</p>
                    <ul>
                        <li>Jobs Discovered: {total_jobs}</li>
                        <li>Matches Found: {total_matches}</li>
                        <li>High Confidence Matches: {high_matches}</li>
                        <li>Pending Applications: {pending_apps}</li>
                        <li>Submitted Applications: {submitted_apps}</li>
                    </ul>
                    <p><a href="http://localhost:3000">Open Dashboard</a></p>
                </body>
            </html>
            """
            
            email_service.send_email(
                to="me",
                subject=f"Orbiter Daily Digest - {today}",
                body=html_body,
                html=True
            )
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Digest agent failed: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            db.close()

digest_agent = DigestAgent()
