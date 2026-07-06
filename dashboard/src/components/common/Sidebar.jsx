import React from 'react';
import { NavLink } from 'react-router-dom';

const tabs = [
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/quickstart', label: 'Quick Start Guide' },
  { path: '/jobs', label: 'Jobs Explorer' },
  { path: '/applications', label: 'Applications' },
  { path: '/crm', label: 'Recruiter CRM' },
  { path: '/analytics', label: 'Analytics & Eval' },
  { path: '/operations', label: 'Operations' },
  { path: '/settings', label: 'Settings' },
];

export default function Sidebar() {
  return (
    <div style={{
      width: '250px',
      minWidth: '250px',
      backgroundColor: '#1e293b',
      borderRight: '1px solid rgba(255, 255, 255, 0.1)',
      padding: '20px',
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
    }}>
      <h2 style={{
        margin: 0,
        color: '#f8fafc',
        fontSize: '1.5rem',
        fontWeight: 'bold',
      }}>
        Orbiter
      </h2>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {tabs.map((tab) => (
          <NavLink
            key={tab.path}
            to={tab.path}
            style={({ isActive }) => ({
              textAlign: 'left',
              padding: '10px 16px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: isActive ? 'bold' : 'normal',
              backgroundColor: isActive ? '#3b82f6' : 'transparent',
              color: isActive ? '#ffffff' : '#94a3b8',
              textDecoration: 'none',
              transition: 'all 0.2s ease',
            })}
          >
            {tab.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
