import React from 'react';

export default function DecisionTrace({ job }) {
  const defaultJob = {
    title: 'Senior Python Developer',
    company: 'Fintech Solutions',
    score: 0.88,
    overlap: '85%',
    fidelity: '95%',
    explanation: 'Candidate lists 4+ years of Python, FastAPI, and PostgreSQL experience. The job description highlights FastAPI and server architecture which maps directly to the candidate\'s recent experience. Minor gap in AWS deployment, but strong core alignment matches adjacent domain rules.'
  };

  const activeJob = job || defaultJob;

  return (
    <div className="glass-panel" style={{ padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <h3 style={{ margin: '0 0 15px 0', color: '#f8fafc' }}>🤖 AI Decision Trace — {activeJob.title} at {activeJob.company}</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '15px', marginBottom: '20px' }}>
        <div style={{ textAlign: 'center', padding: '15px', backgroundColor: 'rgba(59, 130, 246, 0.1)', border: '1px solid #3b82f6', borderRadius: '8px' }}>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#3b82f6' }}>{activeJob.score}</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '5px' }}>Cosine Similarity</div>
        </div>
        <div style={{ textAlign: 'center', padding: '15px', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', borderRadius: '8px' }}>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#10b981' }}>{activeJob.overlap}</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '5px' }}>Skill Overlap</div>
        </div>
        <div style={{ textAlign: 'center', padding: '15px', backgroundColor: 'rgba(139, 92, 246, 0.1)', border: '1px solid #8b5cf6', borderRadius: '8px' }}>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#8b5cf6' }}>{activeJob.fidelity}</div>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '5px' }}>Domain Fidelity</div>
        </div>
      </div>
      <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.4)', padding: '15px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)', fontSize: '0.95rem', lineHeight: '1.5', color: '#e2e8f0' }}>
        <strong style={{ color: '#f8fafc', display: 'block', marginBottom: '5px' }}>Decision Explainer:</strong>
        {activeJob.explanation}
      </div>
    </div>
  );
}
