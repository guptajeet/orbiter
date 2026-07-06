import React, { useState, useEffect, useCallback } from 'react';
import { api } from '../utils/api';
import PromptConsole from '../components/ops/PromptConsole';

export default function Analytics() {
  const [tab, setTab] = useState('report');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rawMetrics, setRawMetrics] = useState([]);
  const [totalMetrics, setTotalMetrics] = useState(0);
  const [metricsSkip, setMetricsSkip] = useState(0);
  const [metricsLoading, setMetricsLoading] = useState(false);
  const [metricsError, setMetricsError] = useState(null);

  useEffect(() => {
    loadReport();
  }, []);

  useEffect(() => {
    if (tab === 'metrics') loadMetrics();
  }, [tab, metricsSkip]);

  const loadReport = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/api/evaluation/report');
      setReport(data.report || null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadMetrics = async () => {
    try {
      setMetricsLoading(true);
      setMetricsError(null);
      const data = await api.get('/api/evaluation/metrics?skip=' + metricsSkip + '&limit=50');
      setRawMetrics(data.metrics || []);
      setTotalMetrics(data.total || 0);
    } catch (err) {
      setMetricsError(err.message);
    } finally {
      setMetricsLoading(false);
    }
  };

  const formatPercent = (val) => {
    if (val == null) return 'N/A';
    return `${(val * 100).toFixed(1)}%`;
  };

  const metrics = report ? [
    { label: 'Match Precision', value: formatPercent(report.match_precision), desc: 'Callbacks on high-confidence matches' },
    { label: 'Callback Rate', value: formatPercent(report.callback_rate), desc: 'Callbacks on all applications' },
    { label: 'Email Response Rate', value: formatPercent(report.email_response_rate), desc: 'Replies on recruiter emails sent' }
  ] : [];

  const totalPages = Math.ceil(totalMetrics / 50);

  const tabBtnStyle = (active) => ({
    padding: '10px 24px',
    borderRadius: '9999px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: active ? 'bold' : 'normal',
    color: active ? '#f8fafc' : '#94a3b8',
    backgroundColor: active ? '#3b82f6' : 'rgba(30, 41, 59, 0.7)',
    transition: 'all 0.2s',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div>
        <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>📊 Analytics & Evaluation</h1>
        <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Monitor match precision, A/B variant experiments, and edit prompt files.</p>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button style={tabBtnStyle(tab === 'report')} onClick={() => setTab('report')}>Report</button>
        <button style={tabBtnStyle(tab === 'metrics')} onClick={() => setTab('metrics')}>Raw Metrics</button>
      </div>

      {error && (
        <div style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444' }}>
          {error}
        </div>
      )}

      {tab === 'report' && (
        <>
          {loading ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
              {[1, 2, 3].map(i => (
                <div key={i} className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)', textAlign: 'center', padding: '40px' }}>
                  <div style={{ color: '#94a3b8' }}>Loading...</div>
                </div>
              ))}
            </div>
          ) : report ? (
            <div style={{ display: 'grid', gridTemplateColumns: `repeat(${metrics.length}, 1fr)`, gap: '20px' }}>
              {metrics.map((m, idx) => (
                <div key={idx} className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
                  <div style={{ fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 'bold' }}>{m.label}</div>
                  <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3b82f6', marginTop: '10px' }}>{m.value}</div>
                  <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '8px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '8px' }}>
                    {m.desc}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8', border: '1px dashed rgba(255, 255, 255, 0.1)', borderRadius: '8px' }}>
              No evaluation report available yet.
            </div>
          )}
          <PromptConsole />
        </>
      )}

      {tab === 'metrics' && (
        <>
          {metricsError && (
            <div style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444' }}>
              {metricsError}
            </div>
          )}

          <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)', overflow: 'auto' }}>
            {metricsLoading ? (
              <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>Loading metrics...</div>
            ) : rawMetrics.length === 0 ? (
              <div style={{ padding: '40px', textAlign: 'center', color: '#94a3b8' }}>No raw metrics available.</div>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', color: '#f8fafc' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', textAlign: 'left' }}>
                    <th style={{ padding: '12px 16px', color: '#94a3b8', fontWeight: '600' }}>Metric Name</th>
                    <th style={{ padding: '12px 16px', color: '#94a3b8', fontWeight: '600' }}>Value</th>
                    <th style={{ padding: '12px 16px', color: '#94a3b8', fontWeight: '600' }}>Context</th>
                    <th style={{ padding: '12px 16px', color: '#94a3b8', fontWeight: '600' }}>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {rawMetrics.map((m) => (
                    <tr key={m.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '10px 16px', color: '#cbd5e1' }}>{m.metric_name}</td>
                      <td style={{ padding: '10px 16px', color: '#3b82f6', fontWeight: 'bold' }}>{m.value}</td>
                      <td style={{ padding: '10px 16px', color: '#94a3b8', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {m.context ? (typeof m.context === 'object' ? JSON.stringify(m.context) : String(m.context)) : '-'}
                      </td>
                      <td style={{ padding: '10px 16px', color: '#94a3b8' }}>{new Date(m.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {totalMetrics > 50 && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
              <button
                disabled={metricsSkip === 0}
                onClick={() => setMetricsSkip((s) => Math.max(0, s - 50))}
                style={{
                  padding: '8px 20px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: metricsSkip === 0 ? 'not-allowed' : 'pointer',
                  backgroundColor: metricsSkip === 0 ? 'rgba(30,41,59,0.4)' : '#1e293b',
                  color: metricsSkip === 0 ? '#475569' : '#f8fafc',
                }}
              >
                Previous
              </button>
              <span style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
                Page {Math.floor(metricsSkip / 50) + 1} of {totalPages}
              </span>
              <button
                disabled={metricsSkip + 50 >= totalMetrics}
                onClick={() => setMetricsSkip((s) => s + 50)}
                style={{
                  padding: '8px 20px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: metricsSkip + 50 >= totalMetrics ? 'not-allowed' : 'pointer',
                  backgroundColor: metricsSkip + 50 >= totalMetrics ? 'rgba(30,41,59,0.4)' : '#1e293b',
                  color: metricsSkip + 50 >= totalMetrics ? '#475569' : '#f8fafc',
                }}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
