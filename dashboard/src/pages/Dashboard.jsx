import React, { useState, useEffect, useRef } from 'react';
import MissionOverview from '../components/mission/MissionOverview';
import AgentTimeline from '../components/mission/AgentTimeline';
import { api } from '../utils/api';

const statusConfig = {
  online: { color: '#10b981', label: 'System Online' },
  offline: { color: '#ef4444', label: 'System Offline' },
  checking: { color: '#f59e0b', label: 'Checking...' },
};

export default function Dashboard() {
  const [healthStatus, setHealthStatus] = useState('checking');
  const intervalRef = useRef(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await api.get('/api/health');
        setHealthStatus(res.status === 'online' ? 'online' : 'offline');
      } catch {
        setHealthStatus('offline');
      }
    };

    fetchHealth();
    intervalRef.current = setInterval(fetchHealth, 30000);

    return () => clearInterval(intervalRef.current);
  }, []);

  const { color, label } = statusConfig[healthStatus];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>Mission Control</h1>
          <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Real-time execution status of autonomous job search supervisors.</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <div style={{ backgroundColor: `${color}15`, color, padding: '8px 16px', borderRadius: '20px', fontWeight: 'bold', fontSize: '0.9rem', border: `1px solid ${color}`, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: color, display: 'inline-block', boxShadow: `0 0 6px ${color}` }} />
            {label}
          </div>
        </div>
      </div>

      <MissionOverview />
      <AgentTimeline />
    </div>
  );
}
