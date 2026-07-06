import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../utils/api';

export default function MissionOverview() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/api/dashboard/metrics')
      .then(setMetrics)
      .catch(() => setMetrics({
        new_matches: 0, auto_applied: 0, review_needed: 0, total_jobs: 0,
        total_applications: 0, interviews: 0, high_confidence_matches: 0,
        agent_status: { master: 'offline', match_engine: 'offline', resume_tailor: 'offline', email_monitor: 'offline' }
      }))
      .finally(() => setLoading(false));
  }, []);

  const statusColor = (s) => s === 'online' ? '#10b981' : '#ef4444';

  if (loading) return <div style={{ color: '#94a3b8' }}>Loading...</div>;

  const hasData = (metrics?.total_jobs > 0) || (metrics?.total_applications > 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Quick Start — only shown when no data */}
      {!hasData && (
        <div className="glass-panel" style={{
          backgroundColor: 'rgba(59, 130, 246, 0.05)',
          border: '1px solid rgba(59, 130, 246, 0.3)',
          padding: '25px 30px',
        }}>
          <h3 style={{ margin: '0 0 5px 0', color: '#f8fafc', fontSize: '1.1rem' }}>Quick Start — Get Running in 3 Steps</h3>
          <p style={{ margin: '0 0 20px 0', color: '#94a3b8', fontSize: '0.85rem' }}>
            Follow these steps to start finding and applying to jobs automatically.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
            {[
              { step: 1, title: 'Upload Resume', desc: 'Go to Settings and upload your PDF or DOCX resume. AI will parse your skills and experience.', link: '/settings', btn: 'Go to Settings' },
              { step: 2, title: 'Discover Jobs', desc: 'Go to Jobs and click "Discover Jobs" to pull listings from RSS feeds and job boards.', link: '/jobs', btn: 'Go to Jobs' },
              { step: 3, title: 'Review Matches', desc: 'Come back here to see matched jobs. Approve or reject applications in the Applications tab.', link: '/applications', btn: 'Go to Applications' },
            ].map((item) => (
              <div key={item.step} style={{
                backgroundColor: 'rgba(15, 23, 42, 0.4)',
                borderRadius: '10px',
                padding: '20px',
                border: '1px solid rgba(255, 255, 255, 0.05)',
              }}>
                <div style={{
                  width: '32px', height: '32px', borderRadius: '50%',
                  backgroundColor: '#3b82f6', color: 'white',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontWeight: 'bold', fontSize: '0.9rem', marginBottom: '12px',
                }}>
                  {item.step}
                </div>
                <div style={{ fontWeight: 'bold', color: '#f8fafc', marginBottom: '6px', fontSize: '0.95rem' }}>
                  {item.title}
                </div>
                <div style={{ color: '#94a3b8', fontSize: '0.8rem', lineHeight: '1.4', marginBottom: '12px' }}>
                  {item.desc}
                </div>
                <button
                  onClick={() => navigate(item.link)}
                  style={{
                    backgroundColor: 'rgba(59, 130, 246, 0.15)',
                    color: '#60a5fa',
                    border: '1px solid rgba(59, 130, 246, 0.3)',
                    padding: '6px 14px',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '0.8rem',
                    fontWeight: 'bold',
                  }}
                >
                  {item.btn} →
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="glass-panel">
          <h3 style={{ margin: '0 0 15px 0' }}>System Status</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
            <div>
              <div style={{ fontSize: '1.8em', fontWeight: 'bold' }}>{metrics?.total_jobs ?? 0}</div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Total Jobs</div>
            </div>
            <div>
              <div style={{ fontSize: '1.8em', fontWeight: 'bold' }}>{metrics?.new_matches ?? 0}</div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>New Matches</div>
            </div>
            <div>
              <div style={{ fontSize: '1.8em', fontWeight: 'bold', color: '#10b981' }}>{metrics?.auto_applied ?? 0}</div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Auto-Applied</div>
            </div>
            <div>
              <div style={{ fontSize: '1.8em', fontWeight: 'bold', color: '#f59e0b' }}>{metrics?.review_needed ?? 0}</div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Review Needed</div>
            </div>
            <div>
              <div style={{ fontSize: '1.8em', fontWeight: 'bold', color: '#3b82f6' }}>{metrics?.interviews ?? 0}</div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Interviews</div>
            </div>
            <div>
              <div style={{ fontSize: '1.8em', fontWeight: 'bold', color: '#8b5cf6' }}>{metrics?.total_applications ?? 0}</div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Total Applications</div>
            </div>
          </div>
        </div>

        <div className="glass-panel">
          <h3 style={{ margin: '0 0 15px 0' }}>Agent Health</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            {Object.entries(metrics?.agent_status || {}).map(([name, status]) => (
              <div key={name} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: statusColor(status), display: 'inline-block' }} />
                <span style={{ textTransform: 'capitalize' }}>{name.replace(/_/g, ' ')}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
