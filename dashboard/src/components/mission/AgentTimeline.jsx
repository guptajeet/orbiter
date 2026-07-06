import React, { useState, useEffect } from 'react';
import { api } from '../../utils/api';

export default function AgentTimeline() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/api/dashboard/activity')
      .then((data) => setActivities(data.activity || []))
      .catch(() => setActivities([]))
      .finally(() => setLoading(false));
  }, []);

  const formatTime = (iso) => {
    if (!iso) return '';
    try {
      return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch { return iso; }
  };

  const formatDuration = (ms) => {
    if (!ms) return '';
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(1)}s`;
  };

  const actionColor = (type) => {
    const map = {
      scrape: '#3b82f6', match: '#8b5cf6', tailor: '#f59e0b',
      outreach: '#10b981', qa: '#ef4444', submit: '#10b981',
    };
    return map[type?.toLowerCase()] || '#94a3b8';
  };

  if (loading) {
    return (
      <div className="glass-panel" style={{ marginTop: '20px', padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
        <h3 style={{ margin: '0 0 20px 0', color: '#f8fafc' }}>Real-Time Agent Activity</h3>
        <div style={{ color: '#94a3b8' }}>Loading activity...</div>
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ marginTop: '20px', padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <h3 style={{ margin: '0 0 20px 0', color: '#f8fafc' }}>Real-Time Agent Activity</h3>
      {activities.length === 0 ? (
        <div style={{ color: '#94a3b8', padding: '20px', textAlign: 'center' }}>
          No agent activity yet. Activity will appear here as agents execute pipeline tasks.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {activities.map((entry, idx) => (
            <div key={entry.id || idx} style={{
              display: 'grid',
              gridTemplateColumns: '140px 1fr 120px',
              alignItems: 'center',
              gap: '16px',
              padding: '12px 16px',
              borderRadius: '8px',
              backgroundColor: 'rgba(15, 23, 42, 0.4)',
              border: '1px solid rgba(255, 255, 255, 0.05)',
            }}>
              <div>
                <div style={{ fontWeight: 'bold', color: actionColor(entry.action_type), fontSize: '0.9rem' }}>
                  {entry.agent_id || 'Unknown Agent'}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
                  {entry.action_type || 'action'}
                </div>
              </div>
              <div>
                <div style={{ color: '#f8fafc', fontSize: '0.85rem' }}>
                  {entry.input_summary || 'No input summary'}
                </div>
                {entry.output_summary && (
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginTop: '2px' }}>
                    → {entry.output_summary}
                  </div>
                )}
                <div style={{ display: 'flex', gap: '10px', marginTop: '6px', fontSize: '0.75rem', color: '#94a3b8' }}>
                  {entry.model_used && <span style={{ padding: '1px 6px', backgroundColor: 'rgba(139, 92, 246, 0.15)', color: '#a78bfa', borderRadius: '4px' }}>{entry.model_used}</span>}
                  {entry.confidence_score != null && <span>Confidence: {(entry.confidence_score * 100).toFixed(0)}%</span>}
                </div>
              </div>
              <div style={{ textAlign: 'right', color: '#94a3b8', fontSize: '0.8rem' }}>
                <div>{formatTime(entry.created_at)}</div>
                {entry.duration_ms && <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{formatDuration(entry.duration_ms)}</div>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
