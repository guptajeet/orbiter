import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import WorkflowReplay from '../components/intelligence/WorkflowReplay';
import DecisionTrace from '../components/intelligence/DecisionTrace';

const COLUMNS = [
  { key: 'pending_approval', title: 'Review Needed', color: '#f59e0b' },
  { key: 'submitted', title: 'Applied', color: '#10b981' },
  { key: 'interview', title: 'Interview', color: '#3b82f6' },
  { key: 'rejected', title: 'Rejected', color: '#ef4444' },
  { key: 'offer', title: 'Offer', color: '#8b5cf6' },
];

const STATUS_COLORS = {
  pending_approval: '#f59e0b',
  submitted: '#10b981',
  interview: '#3b82f6',
  rejected: '#ef4444',
  offer: '#8b5cf6',
};

export default function Applications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [acting, setActing] = useState(null);
  const [selectedApp, setSelectedApp] = useState(null);
  const [appDetail, setAppDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const fetchApps = () => {
    api.get('/api/applications')
      .then((data) => setApplications(data.applications || []))
      .catch(() => setApplications([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchApps(); }, []);

  const handleAction = async (appId, action) => {
    try {
      setActing(appId);
      await api.post(`/api/applications/${appId}/${action}`);
      fetchApps();
    } catch (err) {
      console.error(`Failed to ${action}:`, err);
    } finally {
      setActing(null);
    }
  };

  const handleCardClick = async (app) => {
    setSelectedApp(app);
    setAppDetail(null);
    setDetailLoading(true);
    try {
      const data = await api.get('/api/applications/' + app.id);
      setAppDetail(data);
    } catch (err) {
      console.error('Failed to fetch application detail:', err);
      setAppDetail(app);
    } finally {
      setDetailLoading(false);
    }
  };

  const closeModal = () => {
    setSelectedApp(null);
    setAppDetail(null);
  };

  const grouped = COLUMNS.reduce((acc, col) => {
    acc[col.key] = applications.filter((a) => a.status === col.key);
    return acc;
  }, {});

  const timeAgo = (iso) => {
    if (!iso) return '';
    try {
      const diff = Date.now() - new Date(iso).getTime();
      const mins = Math.floor(diff / 60000);
      if (mins < 1) return 'Just now';
      if (mins < 60) return `${mins}m ago`;
      const hrs = Math.floor(mins / 60);
      if (hrs < 24) return `${hrs}h ago`;
      return `${Math.floor(hrs / 24)}d ago`;
    } catch { return iso; }
  };

  const formatDateTime = (iso) => {
    if (!iso) return 'N/A';
    try {
      return new Date(iso).toLocaleString();
    } catch { return iso; }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div>
        <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>Applications Board</h1>
        <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Monitor matches through the application pipeline, review draft tailoring, and review run logs.</p>
      </div>

      {loading ? (
        <div style={{ color: '#94a3b8', padding: '40px', textAlign: 'center' }}>Loading applications...</div>
      ) : applications.length === 0 ? (
        <div style={{
          color: '#94a3b8',
          padding: '60px 20px',
          textAlign: 'center',
          backgroundColor: 'rgba(30, 41, 59, 0.7)',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }}>
          No applications yet. Applications appear after job matching.
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: `repeat(${COLUMNS.length}, 1fr)`, gap: '15px', marginTop: '20px' }}>
          {COLUMNS.map((col) => (
            <div key={col.key} style={{
              backgroundColor: '#1e293b',
              borderRadius: '12px',
              padding: '15px',
              border: '1px solid rgba(255, 255, 255, 0.05)',
              minHeight: '400px'
            }}>
              <h4 style={{
                margin: '0 0 15px 0',
                color: col.color,
                fontSize: '1rem',
                borderBottom: `2px solid ${col.color}`,
                paddingBottom: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span>{col.title}</span>
                <span style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  color: '#ffffff',
                  borderRadius: '10px',
                  padding: '2px 8px',
                  fontSize: '0.8rem'
                }}>
                  {grouped[col.key].length}
                </span>
              </h4>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {grouped[col.key].map((app) => (
                  <div key={app.id} onClick={() => handleCardClick(app)} style={{
                    backgroundColor: '#0f172a',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    padding: '12px',
                    cursor: 'pointer',
                    transition: 'transform 0.15s ease, border-color 0.15s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.borderColor = '#3b82f6';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'none';
                    e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                  }}>
                    <div style={{ fontWeight: 'bold', fontSize: '0.9rem', color: '#f8fafc' }}>
                      Application #{app.id?.slice(0, 8) || app.id}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '4px' }}>
                      {app.submission_method && <span>via {app.submission_method}</span>}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '6px' }}>
                      {app.submitted_at && <div>Submitted: {timeAgo(app.submitted_at)}</div>}
                      {app.status_updated_at && <div>Updated: {timeAgo(app.status_updated_at)}</div>}
                    </div>
                    {app.source_url && (
                      <a href={app.source_url} target="_blank" rel="noopener noreferrer" style={{
                        display: 'inline-block',
                        marginTop: '8px',
                        color: '#60a5fa',
                        fontSize: '0.75rem',
                        textDecoration: 'none',
                      }}>
                        View Source ↗
                      </a>
                    )}
                    {app.status === 'pending_approval' && (
                      <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
                        <button
                          onClick={(e) => { e.stopPropagation(); handleAction(app.id, 'approve'); }}
                          disabled={acting === app.id}
                          style={{
                            flex: 1,
                            padding: '6px 10px',
                            borderRadius: '6px',
                            border: 'none',
                            backgroundColor: acting === app.id ? '#334155' : '#10b981',
                            color: 'white',
                            fontWeight: 'bold',
                            fontSize: '0.75rem',
                            cursor: acting === app.id ? 'not-allowed' : 'pointer',
                          }}
                        >
                          {acting === app.id ? '...' : 'Approve'}
                        </button>
                        <button
                          onClick={(e) => { e.stopPropagation(); handleAction(app.id, 'reject'); }}
                          disabled={acting === app.id}
                          style={{
                            flex: 1,
                            padding: '6px 10px',
                            borderRadius: '6px',
                            border: 'none',
                            backgroundColor: acting === app.id ? '#334155' : '#ef4444',
                            color: 'white',
                            fontWeight: 'bold',
                            fontSize: '0.75rem',
                            cursor: acting === app.id ? 'not-allowed' : 'pointer',
                          }}
                        >
                          {acting === app.id ? '...' : 'Reject'}
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '30px', marginTop: '10px', alignItems: 'start' }}>
        <WorkflowReplay />
        <DecisionTrace />
      </div>

      {selectedApp && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }} onClick={closeModal}>
          <div onClick={(e) => e.stopPropagation()} style={{
            backgroundColor: '#1e293b',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '16px',
            padding: '28px',
            width: '560px',
            maxHeight: '80vh',
            overflowY: 'auto',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, color: '#f8fafc', fontSize: '1.3rem', fontWeight: 'bold' }}>
                Application #{(appDetail?.id || selectedApp.id)?.slice(0, 8)}
              </h2>
              <button onClick={closeModal} style={{
                background: 'none',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                color: '#94a3b8',
                fontSize: '1.2rem',
                cursor: 'pointer',
                borderRadius: '8px',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background-color 0.15s ease',
              }}
              onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.1)'; }}
              onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'transparent'; }}>
                ✕
              </button>
            </div>

            {detailLoading ? (
              <div style={{ color: '#94a3b8', padding: '40px', textAlign: 'center' }}>Loading details...</div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{
                  padding: '14px',
                  backgroundColor: '#0f172a',
                  borderRadius: '10px',
                  border: '1px solid rgba(255, 255, 255, 0.06)',
                }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                    <div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>Job ID</div>
                      <div style={{ color: '#f8fafc', fontSize: '0.9rem', fontWeight: 500 }}>{appDetail?.job_id || 'N/A'}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>Status</div>
                      <span style={{
                        display: 'inline-block',
                        padding: '3px 10px',
                        borderRadius: '6px',
                        fontSize: '0.8rem',
                        fontWeight: 600,
                        color: '#fff',
                        backgroundColor: STATUS_COLORS[appDetail?.status] || '#64748b',
                      }}>
                        {(appDetail?.status || 'unknown').replace(/_/g, ' ')}
                      </span>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>Submission Method</div>
                      <div style={{ color: '#f8fafc', fontSize: '0.9rem' }}>{appDetail?.submission_method || 'N/A'}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>Submitted At</div>
                      <div style={{ color: '#f8fafc', fontSize: '0.9rem' }}>{formatDateTime(appDetail?.submitted_at)}</div>
                    </div>
                  </div>
                  {appDetail?.source_url && (
                    <div style={{ marginTop: '12px' }}>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>Source URL</div>
                      <a href={appDetail.source_url} target="_blank" rel="noopener noreferrer" style={{ color: '#3b82f6', fontSize: '0.85rem', textDecoration: 'none', wordBreak: 'break-all' }}>
                        {appDetail.source_url}
                      </a>
                    </div>
                  )}
                  {appDetail?.status_updated_at && (
                    <div style={{ marginTop: '12px' }}>
                      <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px' }}>Last Updated</div>
                      <div style={{ color: '#f8fafc', fontSize: '0.9rem' }}>{formatDateTime(appDetail.status_updated_at)}</div>
                    </div>
                  )}
                </div>

                {appDetail?.tailored_resume && (
                  <div style={{
                    padding: '14px',
                    backgroundColor: '#0f172a',
                    borderRadius: '10px',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                      <div style={{ fontSize: '0.7rem', color: '#10b981', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 600 }}>Tailored Resume</div>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <a 
                          href={`/api/applications/${appDetail.id || selectedApp.id}/export?type=resume&format=pdf`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '0.7rem',
                            color: '#10b981',
                            textDecoration: 'none',
                            backgroundColor: 'rgba(16, 185, 129, 0.08)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(16, 185, 129, 0.25)',
                            transition: 'all 0.15s ease',
                            fontWeight: 600
                          }}
                          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(16, 185, 129, 0.18)'; }}
                          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(16, 185, 129, 0.08)'; }}
                        >
                          📄 PDF
                        </a>
                        <a 
                          href={`/api/applications/${appDetail.id || selectedApp.id}/export?type=resume&format=docx`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '0.7rem',
                            color: '#10b981',
                            textDecoration: 'none',
                            backgroundColor: 'rgba(16, 185, 129, 0.08)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(16, 185, 129, 0.25)',
                            transition: 'all 0.15s ease',
                            fontWeight: 600
                          }}
                          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(16, 185, 129, 0.18)'; }}
                          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(16, 185, 129, 0.08)'; }}
                        >
                          📝 Word
                        </a>
                        <a 
                          href={`/api/applications/${appDetail.id || selectedApp.id}/export?type=resume&format=md`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '0.7rem',
                            color: '#10b981',
                            textDecoration: 'none',
                            backgroundColor: 'rgba(16, 185, 129, 0.08)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(16, 185, 129, 0.25)',
                            transition: 'all 0.15s ease',
                            fontWeight: 600
                          }}
                          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(16, 185, 129, 0.18)'; }}
                          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(16, 185, 129, 0.08)'; }}
                        >
                          Ⓜ️ MD
                        </a>
                      </div>
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.82rem', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                      {appDetail.tailored_resume}
                    </div>
                  </div>
                )}

                {appDetail?.cover_letter && (
                  <div style={{
                    padding: '14px',
                    backgroundColor: '#0f172a',
                    borderRadius: '10px',
                    border: '1px solid rgba(59, 130, 246, 0.2)',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                      <div style={{ fontSize: '0.7rem', color: '#3b82f6', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 600 }}>Cover Letter</div>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <a 
                          href={`/api/applications/${appDetail.id || selectedApp.id}/export?type=cover_letter&format=pdf`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '0.7rem',
                            color: '#3b82f6',
                            textDecoration: 'none',
                            backgroundColor: 'rgba(59, 130, 246, 0.08)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(59, 130, 246, 0.25)',
                            transition: 'all 0.15s ease',
                            fontWeight: 600
                          }}
                          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.18)'; }}
                          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.08)'; }}
                        >
                          📄 PDF
                        </a>
                        <a 
                          href={`/api/applications/${appDetail.id || selectedApp.id}/export?type=cover_letter&format=docx`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '0.7rem',
                            color: '#3b82f6',
                            textDecoration: 'none',
                            backgroundColor: 'rgba(59, 130, 246, 0.08)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(59, 130, 246, 0.25)',
                            transition: 'all 0.15s ease',
                            fontWeight: 600
                          }}
                          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.18)'; }}
                          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.08)'; }}
                        >
                          📝 Word
                        </a>
                        <a 
                          href={`/api/applications/${appDetail.id || selectedApp.id}/export?type=cover_letter&format=txt`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          style={{
                            fontSize: '0.7rem',
                            color: '#3b82f6',
                            textDecoration: 'none',
                            backgroundColor: 'rgba(59, 130, 246, 0.08)',
                            padding: '2px 6px',
                            borderRadius: '4px',
                            border: '1px solid rgba(59, 130, 246, 0.25)',
                            transition: 'all 0.15s ease',
                            fontWeight: 600
                          }}
                          onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.18)'; }}
                          onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'rgba(59, 130, 246, 0.08)'; }}
                        >
                          🔤 Text
                        </a>
                      </div>
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.82rem', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                      {appDetail.cover_letter}
                    </div>
                  </div>
                )}

                {appDetail?.tracking_events && appDetail.tracking_events.length > 0 && (
                  <div style={{
                    padding: '14px',
                    backgroundColor: '#0f172a',
                    borderRadius: '10px',
                    border: '1px solid rgba(255, 255, 255, 0.06)',
                  }}>
                    <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px', fontWeight: 600 }}>Tracking Events</div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {appDetail.tracking_events.map((event, idx) => (
                        <div key={idx} style={{
                          padding: '10px',
                          backgroundColor: '#1e293b',
                          borderRadius: '8px',
                          border: '1px solid rgba(255,255,255,0.04)',
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                            <span style={{ color: '#3b82f6', fontSize: '0.8rem', fontWeight: 600 }}>{event.event_type}</span>
                            <span style={{ color: '#64748b', fontSize: '0.7rem' }}>{formatDateTime(event.created_at)}</span>
                          </div>
                          {event.details && (
                            <div style={{ color: '#94a3b8', fontSize: '0.78rem', lineHeight: 1.5 }}>
                              {typeof event.details === 'string' ? event.details : JSON.stringify(event.details)}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {!appDetail?.tailored_resume && !appDetail?.cover_letter && (!appDetail?.tracking_events || appDetail.tracking_events.length === 0) && (
                  <div style={{ color: '#64748b', textAlign: 'center', padding: '20px', fontSize: '0.85rem' }}>
                    No additional details available for this application.
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
