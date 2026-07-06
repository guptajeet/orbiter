import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import ChaosConsole from '../components/ops/ChaosConsole';

const modeMeta = {
  advisor: {
    name: '🔍 Advisor Mode',
    desc: 'Discover jobs and score matches. Never tailor resumes, draft emails, or submit forms. Everything stays in review queue.',
    color: '#94a3b8'
  },
  copilot: {
    name: '🤝 Copilot Mode',
    desc: 'Discover, score, and compose tailored resumes + cover letters. Queues all proposals for manual click-approvals in dashboard before sending.',
    color: '#f59e0b'
  },
  autopilot: {
    name: '🚀 Autopilot Mode',
    desc: 'Full autonomous operations. Auto-tailors and auto-submits applications above 80% confidence tier. Flags edge cases in Daily Digest.',
    color: '#10b981'
  }
};

export default function Operations() {
  const [currentMode, setCurrentMode] = useState('copilot');
  const [availableModes, setAvailableModes] = useState([]);
  const [modeConfig, setModeConfig] = useState(null);
  const [confidenceThreshold, setConfidenceThreshold] = useState(null);
  const [loading, setLoading] = useState(true);
  const [switching, setSwitching] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMode();
  }, []);

  const loadMode = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/api/mode');
      setCurrentMode(data.current_mode);
      setAvailableModes(data.available_modes || ['advisor', 'copilot', 'autopilot']);
      setModeConfig(data.mode_config);
      setConfidenceThreshold(data.confidence_threshold);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const switchMode = async (newMode) => {
    if (newMode === currentMode || switching) return;
    try {
      setSwitching(true);
      setError(null);
      await api.put('/api/mode', { mode: newMode });
      setCurrentMode(newMode);
    } catch (err) {
      setError(err.message);
    } finally {
      setSwitching(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div>
        <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>⚙️ Systems Operations</h1>
        <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Adjust automation thresholds, switch modes, and toggle engineering chaos injection.</p>
      </div>

      {error && (
        <div style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444' }}>
          {error}
        </div>
      )}

      {/* Mode selectors */}
      <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h3 style={{ margin: 0, color: '#f8fafc' }}>Automation Mode Engine Selection</h3>
          {confidenceThreshold != null && (
            <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
              Confidence threshold: <strong style={{ color: '#3b82f6' }}>{(confidenceThreshold * 100).toFixed(0)}%</strong>
            </span>
          )}
        </div>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>Loading mode...</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
            {availableModes.map((modeId) => {
              const m = modeMeta[modeId] || { name: modeId, desc: '', color: '#94a3b8' };
              const isActive = currentMode === modeId;
              return (
                <div
                  key={modeId}
                  onClick={() => switchMode(modeId)}
                  style={{
                    padding: '20px',
                    borderRadius: '12px',
                    backgroundColor: isActive ? `${m.color}15` : 'rgba(255, 255, 255, 0.02)',
                    border: isActive ? `2px solid ${m.color}` : '2px solid rgba(255, 255, 255, 0.05)',
                    cursor: switching ? 'not-allowed' : 'pointer',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    opacity: switching ? 0.6 : 1
                  }}
                >
                  <div>
                    <h4 style={{ margin: 0, color: '#f8fafc', fontSize: '1.1rem' }}>{m.name}</h4>
                    <p style={{ margin: '10px 0 0 0', fontSize: '0.85rem', color: '#cbd5e1', lineHeight: '1.4' }}>{m.desc}</p>
                  </div>
                  {isActive && (
                    <div style={{ marginTop: '15px', fontWeight: 'bold', color: m.color, fontSize: '0.85rem', alignSelf: 'flex-end' }}>
                      ✓ ACTIVE ENGINE
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Chaos simulator */}
      <ChaosConsole />
    </div>
  );
}
