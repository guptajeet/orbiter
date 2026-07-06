import logging
from backend.memory.store import memory_store
from backend.ai_gateway.gateway import ai_gateway

logger = logging.getLogger(__name__)

class FeedbackProcessor:
    def process_user_action(self, action_type: str, context: dict):
        """Converts user approvals/rejections into agent memories"""
        if action_type == "approve_application":
            memory_type = "approval_pattern"
            agent_id = "master"
            # Summarize the approval
            content = {"job_title": context.get("job_title"), "company": context.get("company"), "approved": True}
        elif action_type == "reject_application":
            memory_type = "rejection_pattern"
            agent_id = "master"
            content = {"job_title": context.get("job_title"), "company": context.get("company"), "reason": context.get("reason", "unknown")}
        else:
            return
            
        # Get embedding for the job title to store in memory
        try:
            embedding = ai_gateway.embed("embedding", context.get("job_title", ""))
            memory_store.remember(agent_id, memory_type, content, embedding)
        except Exception as e:
            logger.error(f"Failed to process feedback: {e}")

feedback_processor = FeedbackProcessor()
