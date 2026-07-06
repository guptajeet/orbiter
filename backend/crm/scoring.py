from backend.crm.models import RecruiterContact, Conversation

class CRMScorer:
    def compute_score(self, contact: RecruiterContact, db_session) -> float:
        # Simplistic MVP scoring
        convos = db_session.query(Conversation).filter(Conversation.contact_id == contact.id).all()
        if not convos:
            return 0.0
            
        inbound = 0
        outbound = 0
        for convo in convos:
            for msg in convo.messages:
                if msg.get("direction") == "inbound":
                    inbound += 1
                else:
                    outbound += 1
                    
        if outbound == 0:
            return 1.0 if inbound > 0 else 0.0
            
        response_rate = min(1.0, inbound / outbound)
        return round(response_rate, 2)

crm_scorer = CRMScorer()
