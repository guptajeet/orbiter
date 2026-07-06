import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';

export default function CRM() {
  const [contacts, setContacts] = useState([]);
  const [selectedContact, setSelectedContact] = useState(null);
  const [contactDetail, setContactDetail] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [loadingContacts, setLoadingContacts] = useState(true);
  const [loadingConversations, setLoadingConversations] = useState(false);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newContact, setNewContact] = useState({ name: '', email: '', company: '', title: '', source: 'manual' });
  const [savingContact, setSavingContact] = useState(false);
  const [logContent, setLogContent] = useState('');
  const [loggingMessage, setLoggingMessage] = useState(false);

  useEffect(() => {
    loadContacts();
  }, []);

  useEffect(() => {
    if (selectedContact) {
      loadConversations(selectedContact.id);
      loadContactDetail(selectedContact.id);
    }
  }, [selectedContact]);

  const loadContacts = async () => {
    try {
      setLoadingContacts(true);
      setError(null);
      const data = await api.get('/api/crm/contacts');
      const list = data.contacts || [];
      setContacts(list);
      if (list.length > 0) setSelectedContact(list[0]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingContacts(false);
    }
  };

  const loadContactDetail = async (contactId) => {
    try {
      setLoadingDetail(true);
      const data = await api.get(`/api/crm/contacts/${contactId}`);
      setContactDetail(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingDetail(false);
    }
  };

  const loadConversations = async (contactId) => {
    try {
      setLoadingConversations(true);
      const data = await api.get(`/api/crm/conversations/${contactId}`);
      const list = data.conversations || [];
      setConversations(list);
      if (list.length > 0) setActiveConversation(list[0]);
      else setActiveConversation(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingConversations(false);
    }
  };

  const addContact = async () => {
    if (!newContact.name || !newContact.email) return;
    try {
      setSavingContact(true);
      setError(null);
      await api.post('/api/crm/contacts', {
        name: newContact.name,
        email: newContact.email,
        company: newContact.company,
        title: newContact.title,
        source: newContact.source,
      });
      setShowAddForm(false);
      setNewContact({ name: '', email: '', company: '', title: '', source: 'manual' });
      await loadContacts();
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingContact(false);
    }
  };

  const handleLogMessage = async (direction) => {
    if (!selectedContact) return;
    if (!logContent.trim()) {
      setError("Please enter message content in the textarea before logging.");
      return;
    }
    try {
      setLoggingMessage(true);
      setError(null);
      await api.post(`/api/crm/conversations/${selectedContact.id}/messages`, {
        content: logContent,
        direction: direction
      });
      setLogContent('');
      await loadConversations(selectedContact.id);
      await loadContactDetail(selectedContact.id);
      
      // Also update contacts list to refresh left-panel relationship scores
      const data = await api.get('/api/crm/contacts');
      setContacts(data.contacts || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoggingMessage(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#10b981';
    if (score >= 0.5) return '#f59e0b';
    return '#ef4444';
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  const detailInfoStyle = { display: 'flex', flexDirection: 'column', gap: '6px' };
  const detailLabelStyle = { fontSize: '0.7rem', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#94a3b8' };
  const detailValueStyle = { fontSize: '0.85rem', color: '#f8fafc', wordBreak: 'break-word' };
  const detailRowStyle = { display: 'flex', gap: '24px', flexWrap: 'wrap' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div>
        <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>🤝 Recruiter CRM</h1>
        <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Nurture recruiter relationships, view scoring weights, and manage scheduled check-ins.</p>
      </div>

      {error && (
        <div style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '30px', alignItems: 'start' }}>
        <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
            <h3 style={{ margin: 0, color: '#f8fafc' }}>Recruiter Contacts</h3>
            <button
              onClick={() => setShowAddForm(!showAddForm)}
              style={{
                padding: '6px 12px',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: showAddForm ? '#475569' : '#3b82f6',
                color: 'white',
                fontWeight: 'bold',
                fontSize: '0.8rem',
                cursor: 'pointer',
              }}
            >
              {showAddForm ? 'Cancel' : '+ Add Contact'}
            </button>
          </div>

          {showAddForm && (
            <div style={{ marginBottom: '15px', padding: '15px', borderRadius: '8px', backgroundColor: 'rgba(15, 23, 42, 0.4)', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <input placeholder="Name *" value={newContact.name} onChange={(e) => setNewContact(p => ({...p, name: e.target.value}))} style={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', padding: '8px', borderRadius: '6px', fontSize: '0.85rem' }} />
                <input placeholder="Email *" value={newContact.email} onChange={(e) => setNewContact(p => ({...p, email: e.target.value}))} style={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', padding: '8px', borderRadius: '6px', fontSize: '0.85rem' }} />
                <input placeholder="Company" value={newContact.company} onChange={(e) => setNewContact(p => ({...p, company: e.target.value}))} style={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', padding: '8px', borderRadius: '6px', fontSize: '0.85rem' }} />
                <input placeholder="Title" value={newContact.title} onChange={(e) => setNewContact(p => ({...p, title: e.target.value}))} style={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', padding: '8px', borderRadius: '6px', fontSize: '0.85rem' }} />
                <button
                  onClick={addContact}
                  disabled={savingContact || !newContact.name || !newContact.email}
                  style={{
                    padding: '8px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: savingContact || !newContact.name || !newContact.email ? '#475569' : '#10b981',
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: '0.85rem',
                    cursor: savingContact || !newContact.name || !newContact.email ? 'not-allowed' : 'pointer',
                  }}
                >
                  {savingContact ? 'Saving...' : 'Save Contact'}
                </button>
              </div>
            </div>
          )}
          {loadingContacts ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>Loading contacts...</div>
          ) : contacts.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8', border: '1px dashed rgba(255, 255, 255, 0.1)', borderRadius: '8px' }}>
              No recruiter contacts yet. Add contacts via the CRM API.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {contacts.map((contact) => (
                <div
                  key={contact.id}
                  onClick={() => setSelectedContact(contact)}
                  style={{
                    padding: '12px',
                    borderRadius: '8px',
                    backgroundColor: selectedContact?.id === contact.id ? 'rgba(59, 130, 246, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                    border: selectedContact?.id === contact.id ? '1px solid #3b82f6' : '1px solid rgba(255, 255, 255, 0.05)',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 'bold', color: '#f8fafc' }}>{contact.name}</span>
                    <span style={{
                      fontSize: '0.75rem',
                      fontWeight: 'bold',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      backgroundColor: getScoreColor(contact.relationship_score) + '20',
                      color: getScoreColor(contact.relationship_score)
                    }}>
                      Score: {Math.round(contact.relationship_score * 100)}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#cbd5e1', marginTop: '2px' }}>{contact.company}</div>
                  {contact.title && (
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>{contact.title}</div>
                  )}
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginTop: '8px' }}>
                    <span>Last: {formatDate(contact.last_interaction_at)}</span>
                    <span>{contact.source}</span>
                  </div>
                  {contact.tags && contact.tags.length > 0 && (
                    <div style={{ display: 'flex', gap: '4px', marginTop: '6px', flexWrap: 'wrap' }}>
                      {contact.tags.map((tag, i) => (
                        <span key={i} style={{ fontSize: '0.65rem', padding: '1px 5px', borderRadius: '4px', backgroundColor: 'rgba(59, 130, 246, 0.15)', color: '#3b82f6' }}>
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)', minHeight: '350px', display: 'flex', flexDirection: 'column' }}>
          {selectedContact ? (
            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              <div style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', paddingBottom: '15px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ margin: 0, color: '#f8fafc' }}>Conversation with {selectedContact.name}</h3>
                  <p style={{ margin: '4px 0 0 0', color: '#94a3b8', fontSize: '0.85rem' }}>
                    {selectedContact.email} • {selectedContact.title ? `${selectedContact.title} at ` : ''}{selectedContact.company}
                  </p>
                </div>
                <button
                  onClick={async () => {
                    await loadContacts();
                    await loadConversations(selectedContact.id);
                    await loadContactDetail(selectedContact.id);
                  }}
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    color: '#f8fafc',
                    fontWeight: 'bold',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                  onMouseOver={(e) => e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)'}
                  onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.05)'}
                >
                  🔄 Refresh
                </button>
              </div>

              {loadingDetail ? (
                <div style={{ textAlign: 'center', padding: '20px', color: '#94a3b8', marginBottom: '15px' }}>Loading contact info...</div>
              ) : contactDetail && (
                <div style={{ marginBottom: '20px', padding: '16px', borderRadius: '10px', backgroundColor: 'rgba(15, 23, 42, 0.5)', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#3b82f6', marginBottom: '12px' }}>
                    Contact Info
                  </div>
                  <div style={detailRowStyle}>
                    {contactDetail.phone && (
                      <div style={detailInfoStyle}>
                        <span style={detailLabelStyle}>Phone</span>
                        <span style={detailValueStyle}>{contactDetail.phone}</span>
                      </div>
                    )}
                    {contactDetail.department && (
                      <div style={detailInfoStyle}>
                        <span style={detailLabelStyle}>Department</span>
                        <span style={detailValueStyle}>{contactDetail.department}</span>
                      </div>
                    )}
                    {contactDetail.linkedin_url && (
                      <div style={detailInfoStyle}>
                        <span style={detailLabelStyle}>LinkedIn</span>
                        <a href={contactDetail.linkedin_url} target="_blank" rel="noopener noreferrer" style={{ ...detailValueStyle, color: '#3b82f6', textDecoration: 'none' }}>
                          {contactDetail.linkedin_url}
                        </a>
                      </div>
                    )}
                    {contactDetail.first_contact_at && (
                      <div style={detailInfoStyle}>
                        <span style={detailLabelStyle}>First Contact</span>
                        <span style={detailValueStyle}>{formatDate(contactDetail.first_contact_at)}</span>
                      </div>
                    )}
                  </div>
                  {contactDetail.notes && (
                    <div style={{ ...detailInfoStyle, marginTop: '12px' }}>
                      <span style={detailLabelStyle}>Notes</span>
                      <span style={{ ...detailValueStyle, fontSize: '0.8rem', lineHeight: '1.5', color: '#cbd5e1' }}>{contactDetail.notes}</span>
                    </div>
                  )}
                </div>
              )}

              <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {loadingConversations ? (
                  <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>Loading conversations...</div>
                ) : !activeConversation ? (
                  <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8', border: '1px dashed rgba(255, 255, 255, 0.1)', borderRadius: '8px' }}>
                    No conversations with this contact yet.
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', padding: '10px 0' }}>
                    {(activeConversation.messages || []).map((msg, idx) => (
                      <div key={idx} style={{
                        maxWidth: '70%',
                        alignSelf: msg.direction === 'outbound' ? 'flex-end' : 'flex-start',
                        backgroundColor: msg.direction === 'outbound' ? '#3b82f6' : 'rgba(255, 255, 255, 0.05)',
                        color: '#ffffff',
                        padding: '12px 16px',
                        borderRadius: '12px',
                        borderTopRightRadius: msg.direction === 'outbound' ? '2px' : '12px',
                        borderTopLeftRadius: msg.direction === 'inbound' ? '2px' : '12px'
                      }}>
                        <div style={{ fontSize: '0.9rem', lineHeight: '1.4' }}>{msg.content}</div>
                        <div style={{ textAlign: 'right', fontSize: '0.7rem', color: 'rgba(255, 255, 255, 0.6)', marginTop: '5px' }}>
                          {formatDate(msg.timestamp)}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {activeConversation && (
                <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.1)', paddingTop: '20px', marginTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                    {activeConversation.next_followup_at ? (
                      <>Next follow-up: <strong>{formatDate(activeConversation.next_followup_at)}</strong></>
                    ) : (
                      'No follow-up scheduled.'
                    )}
                  </span>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <span style={{
                      fontSize: '0.75rem',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      backgroundColor: activeConversation.status === 'active' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                      color: activeConversation.status === 'active' ? '#10b981' : '#f59e0b'
                    }}>
                      {activeConversation.status}
                    </span>
                  </div>
                </div>
              )}

              {/* Message Logging Form */}
              <div style={{ marginTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.1)', paddingTop: '15px' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#3b82f6', marginBottom: '8px' }}>
                  Log Interaction
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  <textarea 
                    placeholder="Type email outreach or response content here..."
                    value={logContent}
                    onChange={(e) => setLogContent(e.target.value)}
                    style={{
                      width: '100%',
                      minHeight: '60px',
                      backgroundColor: '#0f172a',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      color: '#ffffff',
                      padding: '8px 12px',
                      borderRadius: '6px',
                      fontSize: '0.85rem',
                      fontFamily: 'inherit',
                      resize: 'none'
                    }}
                  />
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                      onClick={() => handleLogMessage('outbound')}
                      disabled={loggingMessage}
                      style={{
                        flex: 1,
                        padding: '8px 12px',
                        borderRadius: '6px',
                        border: 'none',
                        backgroundColor: loggingMessage ? '#475569' : '#3b82f6',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '0.8rem',
                        cursor: loggingMessage ? 'not-allowed' : 'pointer'
                      }}
                    >
                      Log Outbound Email
                    </button>
                    <button
                      onClick={() => handleLogMessage('inbound')}
                      disabled={loggingMessage}
                      style={{
                        flex: 1,
                        padding: '8px 12px',
                        borderRadius: '6px',
                        border: 'none',
                        backgroundColor: loggingMessage ? '#475569' : '#10b981',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '0.8rem',
                        cursor: loggingMessage ? 'not-allowed' : 'pointer'
                      }}
                    >
                      Log Inbound Reply
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
              Select a contact to view conversations
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
