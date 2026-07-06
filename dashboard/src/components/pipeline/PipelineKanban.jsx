import React from 'react';

export default function PipelineKanban() {
  const columns = [
    {
      title: '🔍 Discovered',
      color: '#94a3b8',
      jobs: [
        { id: 1, title: 'Python Engineer', company: 'GlobalDevs', score: 0.72 },
        { id: 2, title: 'Backend Developer', company: 'LogiCore', score: 0.68 }
      ]
    },
    {
      title: '📋 Review Needed',
      color: '#f59e0b',
      jobs: [
        { id: 3, title: 'Senior FastAPI Developer', company: 'TechCorp', score: 0.82 },
        { id: 4, title: 'Software Engineer (FastAPI/Go)', company: 'FinTech Solutions', score: 0.88 }
      ]
    },
    {
      title: '📝 Composed / Ready',
      color: '#8b5cf6',
      jobs: [
        { id: 5, title: 'Platform Engineer', company: 'CloudSystems', score: 0.92 }
      ]
    },
    {
      title: '🚀 Applied / Tracked',
      color: '#10b981',
      jobs: [
        { id: 6, title: 'Backend Systems Engineer', company: 'Fintech Solutions', score: 0.89 }
      ]
    }
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', marginTop: '20px' }}>
      {columns.map((col, idx) => (
        <div key={idx} style={{
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
              {col.jobs.length}
            </span>
          </h4>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {col.jobs.map((job) => (
              <div key={job.id} style={{
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
                <div style={{ fontWeight: 'bold', fontSize: '0.9rem', color: '#f8fafc' }}>{job.title}</div>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '2px' }}>{job.company}</div>
                <div style={{
                  display: 'inline-block',
                  marginTop: '8px',
                  backgroundColor: 'rgba(59, 130, 246, 0.15)',
                  color: '#60a5fa',
                  fontSize: '0.75rem',
                  fontWeight: 'bold',
                  padding: '2px 6px',
                  borderRadius: '4px'
                }}>
                  Fit: {job.score * 100}%
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
