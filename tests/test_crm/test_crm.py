import pytest
from backend.crm.models import RecruiterContact, Conversation
from backend.crm.scoring import crm_scorer

def test_crm_scoring_no_conversations(db_session):
    contact = RecruiterContact(id="rec_1", name="Sarah", email="sarah@corp.com", source="linkedin")
    db_session.add(contact)
    db_session.commit()

    score = crm_scorer.compute_score(contact, db_session)
    assert score == 0.0

def test_crm_scoring_with_conversations(db_session):
    contact = RecruiterContact(id="rec_2", name="Sarah", email="sarah2@corp.com", source="linkedin")
    db_session.add(contact)
    
    # Create a conversation with 1 outbound and 1 inbound message (100% response rate)
    convo = Conversation(
        id="conv_1",
        contact_id="rec_2",
        messages=[
            {"direction": "outbound", "content": "Hi"},
            {"direction": "inbound", "content": "Hello"}
        ],
        status="active"
    )
    db_session.add(convo)
    db_session.commit()

    score = crm_scorer.compute_score(contact, db_session)
    assert score == 1.0
