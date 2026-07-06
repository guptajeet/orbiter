from backend.crm.models import RecruiterContact

class CRMEnrichment:
    def enrich_from_signature(self, contact: RecruiterContact, signature_text: str):
        # MVP: simple mock of signature enrichment
        if "LinkedIn" in signature_text:
            contact.tags.append("has_linkedin")
            
    def run_enrichment_batch(self):
        pass

crm_enrichment = CRMEnrichment()
