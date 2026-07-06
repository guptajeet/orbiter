import React from 'react';

export default function ConfidenceHeatmap() {
  const sources = ['Adzuna', 'Remotive', 'Custom RSS', 'Recruiter Email'];
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
  
  // Matrix data (confidence scores)
  const data = [
    [0.85, 0.72, 0.45, 0.92],
    [0.90, 0.80, 0.50, 0.88],
    [0.78, 0.85, 0.60, 0.95],
    [0.88, 0.70, 0.55, 0.82],
    [0.92, 0.76, 0.48, 0.90]
  ];

  const getColor = (val) => {
    if (val >= 0.9) return '#10b981';     // High (Green)
    if (val >= 0.75) return '#3b82f6';    // Good (Blue)
    if (val >= 0.6) return '#f59e0b';     // Medium (Yellow)
    return '#ef4444';                     // Low (Red)
  };

  return (
    <div className="glass-panel" style={{ padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <h3 style={{ margin: '0 0 15px 0', color: '#f8fafc' }}>📊 Ingestion Source vs Match Quality Heatmap</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '80px repeat(4, 1fr)', gap: '8px', textAlign: 'center' }}>
        <div></div>
        {sources.map((src, i) => (
          <div key={i} style={{ fontSize: '0.85rem', fontWeight: 'bold', color: '#94a3b8', padding: '5px 0' }}>{src}</div>
        ))}

        {days.map((day, dayIdx) => (
          <React.Fragment key={dayIdx}>
            <div style={{ fontSize: '0.85rem', fontWeight: 'bold', color: '#94a3b8', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {day}
            </div>
            {data[dayIdx].map((val, valIdx) => (
              <div
                key={valIdx}
                style={{
                  backgroundColor: getColor(val),
                  color: '#ffffff',
                  height: '40px',
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  fontSize: '0.85rem',
                  opacity: 0.9,
                  transition: 'transform 0.15s ease',
                  cursor: 'pointer'
                }}
                title={`Confidence score: ${val}`}
                onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
                onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
              >
                {val}
              </div>
            ))}
          </React.Fragment>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '15px', marginTop: '20px', justifyContent: 'center', fontSize: '0.8rem', color: '#94a3b8' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '3px', backgroundColor: '#10b981' }}></div> High (&gt;=0.90)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '3px', backgroundColor: '#3b82f6' }}></div> Good (0.75 - 0.89)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '3px', backgroundColor: '#f59e0b' }}></div> Medium (0.60 - 0.74)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '3px', backgroundColor: '#ef4444' }}></div> Low (&lt;0.60)
        </div>
      </div>
    </div>
  );
}
