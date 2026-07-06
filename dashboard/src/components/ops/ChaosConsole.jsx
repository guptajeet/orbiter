import React, { useState, useEffect } from 'react';
import { api } from '../../utils/api';

export default function ChaosConsole() {
  const [scenarios, setScenarios] = useState([]);
  const [resilienceResult, setResilienceResult] = useState(null);
  const [runningSuite, setRunningSuite] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/api/chaos/scenarios');
      setScenarios(data.scenarios || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleScenario = async (scenario) => {
    try {
      setError(null);
      if (scenario.is_active) {
        await api.post(`/api/chaos/scenarios/${scenario.name}/disable`);
      } else {
        await api.post(`/api/chaos/scenarios/${scenario.name}/enable`, { duration: 60 });
      }
      await loadScenarios();
    } catch (err) {
      setError(err.message);
    }
  };

  const triggerResilienceSuite = async () => {
    try {
      setRunningSuite(true);
      setError(null);
      const result = await api.post('/api/chaos/run-suite');
      setResilienceResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setRunningSuite(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h3 style={{ margin: 0, color: '#f8fafc' }}>🚨 Chaos Engineering & Resilience Simulator</h3>
        <button
          onClick={triggerResilienceSuite}
          disabled={runningSuite}
          style={{
            backgroundColor: runningSuite ? '#475569' : '#dc2626',
            color: 'white',
            fontWeight: 'bold',
            padding: '10px 20px',
            borderRadius: '8px',
            border: 'none',
            cursor: runningSuite ? 'not-allowed' : 'pointer'
          }}
        >
          {runningSuite ? 'Running Resilience Suite...' : '🔥 Run Full Resilience Suite'}
        </button>
      </div>

      {error && (
        <div style={{ padding: '10px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444', marginBottom: '15px', fontSize: '0.85rem' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
        {/* Scenarios List */}
        <div>
          <h4 style={{ margin: '0 0 15px 0', color: '#cbd5e1' }}>Simulate Active Failures</h4>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>Loading scenarios...</div>
          ) : scenarios.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8', border: '1px dashed rgba(255, 255, 255, 0.1)', borderRadius: '8px' }}>
              No chaos scenarios configured.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {scenarios.map((s) => (
                <div key={s.name} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  backgroundColor: s.is_active ? 'rgba(239, 68, 68, 0.05)' : 'rgba(255, 255, 255, 0.02)',
                  border: s.is_active ? '1px solid rgba(239, 68, 68, 0.3)' : '1px solid rgba(255, 255, 255, 0.05)'
                }}>
                  <div>
                    <div style={{ fontWeight: 'bold', color: '#f8fafc', fontSize: '0.95rem' }}>{s.name}</div>
                    {s.description && (
                      <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '2px' }}>{s.description}</div>
                    )}
                    <div style={{ fontSize: '0.75rem', color: s.severity === 'critical' ? '#ef4444' : s.severity === 'high' ? '#f97316' : '#f59e0b', textTransform: 'capitalize', marginTop: '2px' }}>
                      Severity: {s.severity}
                    </div>
                    {s.expires_at && (
                      <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: '2px' }}>
                        Expires: {new Date(s.expires_at).toLocaleString()}
                      </div>
                    )}
                  </div>
                  <button
                    onClick={() => toggleScenario(s)}
                    style={{
                      backgroundColor: s.is_active ? '#ef4444' : '#10b981',
                      color: 'white',
                      padding: '6px 14px',
                      borderRadius: '6px',
                      fontSize: '0.85rem',
                      border: 'none',
                      cursor: 'pointer'
                    }}
                  >
                    {s.is_active ? 'Disable' : 'Enable'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Resilience Suite Results */}
        <div>
          <h4 style={{ margin: '0 0 15px 0', color: '#cbd5e1' }}>Resilience Reports</h4>
          {resilienceResult ? (
            <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.4)', padding: '20px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
              {resilienceResult.summary && (
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px', fontWeight: 'bold' }}>
                  <span style={{ color: '#10b981' }}>Passed: {resilienceResult.summary.passed}</span>
                  <span style={{ color: '#ef4444' }}>Failed: {resilienceResult.summary.failed}</span>
                  <span style={{ color: '#cbd5e1' }}>Total: {resilienceResult.summary.total}</span>
                </div>
              )}
              {resilienceResult.results && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.85rem', fontFamily: 'monospace' }}>
                  {resilienceResult.results.map((det, idx) => (
                    <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255, 255, 255, 0.02)', paddingBottom: '4px' }}>
                      <span style={{ color: '#cbd5e1' }}>{det.scenario}</span>
                      <span style={{ color: det.status === 'pass' ? '#10b981' : '#ef4444', fontWeight: 'bold' }}>
                        {det.status.toUpperCase()}{det.recovery ? ` (${det.recovery})` : ''}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8', border: '1px dashed rgba(255, 255, 255, 0.1)', borderRadius: '8px' }}>
              No resilience report compiled yet. Trigger a suite execution to run chaos scenarios.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
