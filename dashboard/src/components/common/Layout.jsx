import React from 'react';
import Sidebar from './Sidebar';

export default function Layout({ children }) {
  return (
    <div style={{
      display: 'flex',
      height: '100vh',
      width: '100vw',
      overflow: 'hidden',
      backgroundColor: '#0f172a',
    }}>
      <Sidebar />
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '30px',
        color: '#f8fafc',
      }}>
        {children}
      </div>
    </div>
  );
}
