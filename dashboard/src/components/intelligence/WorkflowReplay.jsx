import React, { useState } from 'react';

export default function WorkflowReplay() {
  const steps = [
    { label: '🔍 Ingest', desc: 'Discovered job posting via Remotive API integration', time: '10:00 AM', detail: 'Fetched job ID: rem_88201. Title: Senior Backend Engineer at FinTechCorp.' },
    { label: '📊 Match', desc: 'Evaluated resume semantic fit vs job criteria', time: '10:05 AM', detail: 'Semantic score: 0.89. Key skills overlap: 85% (FastAPI, Redis, Docker).' },
    { label: '📝 Tailor', desc: 'Composed custom bullet points and cover letter', time: '10:12 AM', detail: 'Re-ordered FastAPI bullet points and matched them with the database optimizations requirements.' },
    { label: '✅ QA Verify', desc: 'Executed QA checks to prevent hallucinated text', time: '10:15 AM', detail: 'Hallucination checks completed successfully. Zero discrepancies found vs original resume.' },
    { label: '🚀 Submit', desc: 'Sent application materials to GreenHouse API', time: '10:18 AM', detail: 'Greenhouse API returned candidate ID: gh_99011. Registered application reference successfully.' }
  ];

  const [currentStep, setCurrentStep] = useState(0);

  return (
    <div className="glass-panel" style={{ padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <h3 style={{ margin: '0 0 15px 0', color: '#f8fafc' }}>🎞️ Workflow Replay Viewer</h3>
      
      {/* Step selector */}
      <div style={{ display: 'flex', justifyContent: 'space-between', position: 'relative', marginBottom: '30px', padding: '0 10px' }}>
        <div style={{ position: 'absolute', top: '15px', left: 0, right: 0, height: '4px', backgroundColor: 'rgba(255, 255, 255, 0.1)', zIndex: 0 }}></div>
        <div style={{ position: 'absolute', top: '15px', left: 0, width: `${(currentStep / (steps.length - 1)) * 100}%`, height: '4px', backgroundColor: '#3b82f6', zIndex: 0, transition: 'width 0.3s ease' }}></div>
        
        {steps.map((step, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentStep(idx)}
            style={{
              zIndex: 1,
              width: '34px',
              height: '34px',
              borderRadius: '50%',
              backgroundColor: idx <= currentStep ? '#3b82f6' : '#1e293b',
              color: '#ffffff',
              border: idx === currentStep ? '3px solid #60a5fa' : '1px solid rgba(255, 255, 255, 0.1)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 'bold',
              transition: 'all 0.2s ease',
              padding: 0
            }}
          >
            {idx + 1}
          </button>
        ))}
      </div>

      {/* Step details */}
      <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.4)', padding: '20px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <h4 style={{ margin: 0, color: '#3b82f6', fontSize: '1.2rem' }}>{steps[currentStep].label}</h4>
          <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{steps[currentStep].time}</span>
        </div>
        <p style={{ margin: '0 0 10px 0', color: '#f8fafc', fontWeight: 'bold' }}>{steps[currentStep].desc}</p>
        <div style={{ fontSize: '0.9rem', color: '#cbd5e1', borderLeft: '3px solid #10b981', paddingLeft: '12px', fontFamily: 'monospace' }}>
          {steps[currentStep].detail}
        </div>
      </div>

      {/* Navigation buttons */}
      <div style={{ display: 'flex', gap: '10px', marginTop: '20px', justifyContent: 'flex-end' }}>
        <button
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          style={{
            backgroundColor: 'transparent',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            color: currentStep === 0 ? '#475569' : '#f8fafc',
            cursor: currentStep === 0 ? 'not-allowed' : 'pointer'
          }}
        >
          Previous Step
        </button>
        <button
          onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}
          disabled={currentStep === steps.length - 1}
          style={{
            backgroundColor: '#3b82f6',
            color: '#ffffff',
            cursor: currentStep === steps.length - 1 ? 'not-allowed' : 'pointer'
          }}
        >
          Next Step
        </button>
      </div>
    </div>
  );
}
