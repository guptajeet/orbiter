import React, { useState, useEffect } from 'react';
import { api } from '../../utils/api';

export default function PromptConsole() {
  const [prompts, setPrompts] = useState({});
  const [selectedPromptName, setSelectedPromptName] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createForm, setCreateForm] = useState({ prompt_name: '', content: '', variables: '', author: '' });
  const [creating, setCreating] = useState(false);
  const [acting, setActing] = useState(null);
  const [viewingPrompt, setViewingPrompt] = useState(null);

  const handleCloneVersion = (ver) => {
    setCreateForm({
      prompt_name: selectedPromptName || '',
      content: ver.content || '',
      variables: (ver.variables || []).join(', '),
      author: ver.author || 'system'
    });
    setShowCreateModal(true);
  };

  useEffect(() => {
    loadPrompts();
  }, []);

  const loadPrompts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get('/api/promptops/prompts');
      setPrompts(data.prompts || {});
      const names = Object.keys(data.prompts || {});
      if (names.length > 0 && !selectedPromptName) setSelectedPromptName(names[0]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      setError(null);
      setCreating(true);
      const variables = createForm.variables
        ? createForm.variables.split(',').map(v => v.trim()).filter(Boolean)
        : [];
      await api.post('/api/promptops/prompts', {
        prompt_name: createForm.prompt_name,
        content: createForm.content,
        variables,
        author: createForm.author,
      });
      setShowCreateModal(false);
      setCreateForm({ prompt_name: '', content: '', variables: '', author: '' });
      await loadPrompts();
    } catch (err) {
      setError(err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleActivate = async (promptName, versionId) => {
    try {
      setError(null);
      setActing(versionId);
      await api.post(`/api/promptops/prompts/${promptName}/activate/${versionId}`);
      await loadPrompts();
    } catch (err) {
      setError(err.message);
    } finally {
      setActing(null);
    }
  };

  const handleRollback = async (promptName) => {
    try {
      setError(null);
      setActing('rollback');
      await api.post(`/api/promptops/prompts/${promptName}/rollback`);
      await loadPrompts();
    } catch (err) {
      setError(err.message);
    } finally {
      setActing(null);
    }
  };

  const promptNames = Object.keys(prompts);
  const versions = selectedPromptName ? (prompts[selectedPromptName] || []) : [];
  const activeVersion = versions.find(v => v.is_active);

  const btnBase = {
    padding: '6px 14px',
    borderRadius: '6px',
    border: 'none',
    fontSize: '0.8rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'opacity 0.2s',
    fontFamily: 'inherit',
  };

  return (
    <div className="glass-panel" style={{ padding: '20px', backgroundColor: 'rgba(30, 41, 59, 0.7)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
      <h3 style={{ margin: '0 0 20px 0', color: '#f8fafc' }}>PromptOps Version & Rollback Console</h3>

      {error && (
        <div style={{ padding: '10px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444', marginBottom: '15px', fontSize: '0.85rem' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>Loading prompts...</div>
      ) : promptNames.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#94a3b8', border: '1px dashed rgba(255, 255, 255, 0.1)', borderRadius: '8px' }}>
          No prompts configured yet.
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: '30px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', borderRight: '1px solid rgba(255, 255, 255, 0.1)', paddingRight: '20px' }}>
            {promptNames.map((name) => {
              const versionsList = prompts[name] || [];
              const active = versionsList.find(v => v.is_active);
              return (
                <div
                  key={name}
                  onClick={() => setSelectedPromptName(name)}
                  style={{
                    padding: '12px',
                    borderRadius: '8px',
                    backgroundColor: selectedPromptName === name ? 'rgba(59, 130, 246, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                    border: selectedPromptName === name ? '1px solid #3b82f6' : '1px solid rgba(255, 255, 255, 0.05)',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ fontWeight: 'bold', fontSize: '0.95rem', color: '#f8fafc' }}>{name}</div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginTop: '5px' }}>
                    <span>Active: {active ? `v${active.version}` : 'none'}</span>
                    <span>{versionsList.length} version{versionsList.length !== 1 ? 's' : ''}</span>
                  </div>
                </div>
              );
            })}
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <h4 style={{ margin: 0, color: '#f8fafc', fontSize: '1.2rem' }}>{selectedPromptName} versioning</h4>
                <button
                  onClick={() => setShowCreateModal(true)}
                  style={{ ...btnBase, backgroundColor: '#3b82f6', color: '#fff' }}
                >
                  Create New Version
                </button>
              </div>
              {activeVersion && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ fontSize: '0.85rem', color: '#cbd5e1', padding: '4px 10px', backgroundColor: '#3b82f6', borderRadius: '12px', fontWeight: 'bold' }}>
                    Active Version: v{activeVersion.version}
                  </span>
                  <button
                    onClick={() => handleRollback(selectedPromptName)}
                    disabled={acting === 'rollback'}
                    style={{ ...btnBase, backgroundColor: '#ef4444', color: '#fff', opacity: acting === 'rollback' ? 0.5 : 1 }}
                  >
                    {acting === 'rollback' ? 'Rolling...' : 'Rollback'}
                  </button>
                </div>
              )}
            </div>

            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem', marginBottom: '20px' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', color: '#94a3b8' }}>
                  <th style={{ padding: '10px' }}>Version</th>
                  <th style={{ padding: '10px' }}>Author</th>
                  <th style={{ padding: '10px' }}>Content</th>
                  <th style={{ padding: '10px' }}>Status</th>
                  <th style={{ padding: '10px' }}>Created</th>
                  <th style={{ padding: '10px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {versions.map((ver) => (
                  <tr key={ver.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                    <td style={{ padding: '12px', fontWeight: 'bold', color: '#3b82f6' }}>v{ver.version}</td>
                    <td style={{ padding: '12px', color: '#e2e8f0' }}>{ver.author}</td>
                    <td
                      onClick={() => setViewingPrompt(ver)}
                      style={{
                        padding: '12px',
                        color: '#cbd5e1',
                        maxWidth: '250px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        cursor: 'pointer',
                        textDecoration: 'underline dotted rgba(255,255,255,0.3)',
                      }}
                      title="Click to view full content"
                    >
                      {ver.content || '—'}
                    </td>
                    <td style={{ padding: '12px' }}>
                      <span style={{
                        fontSize: '0.75rem',
                        fontWeight: 'bold',
                        padding: '2px 8px',
                        borderRadius: '10px',
                        backgroundColor: ver.is_active ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                        color: ver.is_active ? '#10b981' : '#94a3b8'
                      }}>
                        {ver.is_active ? 'active' : 'inactive'}
                      </span>
                    </td>
                    <td style={{ padding: '12px', color: '#94a3b8', fontSize: '0.8rem' }}>
                      {ver.created_at ? new Date(ver.created_at).toLocaleDateString() : '—'}
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ display: 'flex', gap: '6px' }}>
                        <button
                          onClick={() => setViewingPrompt(ver)}
                          style={{ ...btnBase, backgroundColor: '#475569', color: '#fff' }}
                        >
                          View
                        </button>
                        <button
                          onClick={() => handleCloneVersion(ver)}
                          style={{ ...btnBase, backgroundColor: '#0284c7', color: '#fff' }}
                        >
                          Edit
                        </button>
                        {!ver.is_active && (
                          <button
                            onClick={() => handleActivate(selectedPromptName, ver.id)}
                            disabled={acting === ver.id}
                            style={{ ...btnBase, backgroundColor: '#10b981', color: '#fff', opacity: acting === ver.id ? 0.5 : 1 }}
                          >
                            {acting === ver.id ? 'Activating...' : 'Activate'}
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {activeVersion && activeVersion.performance_metrics && (
              <div style={{ marginTop: '15px', padding: '12px', backgroundColor: 'rgba(15, 23, 42, 0.4)', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <div style={{ fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 'bold', marginBottom: '8px' }}>Performance Metrics</div>
                <div style={{ display: 'flex', gap: '15px', fontSize: '0.8rem', color: '#94a3b8' }}>
                  {Object.entries(activeVersion.performance_metrics).map(([key, val]) => (
                    <span key={key}>{key}: <strong style={{ color: '#3b82f6' }}>{typeof val === 'number' ? val.toFixed(2) : val}</strong></span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {showCreateModal && (
        <div
          style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}
          onClick={(e) => { if (e.target === e.currentTarget) setShowCreateModal(false); }}
        >
          <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)', padding: '24px', width: '480px', maxHeight: '80vh', overflowY: 'auto' }}>
            <h4 style={{ margin: '0 0 18px 0', color: '#f8fafc', fontSize: '1.1rem' }}>Create New Version</h4>

            <div style={{ marginBottom: '14px' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '5px', fontWeight: '600' }}>Prompt Name</label>
              <input
                type="text"
                value={createForm.prompt_name}
                onChange={(e) => setCreateForm({ ...createForm, prompt_name: e.target.value })}
                placeholder="e.g. greeting"
                style={{ width: '100%', padding: '9px 12px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.1)', backgroundColor: 'rgba(15,23,42,0.6)', color: '#f8fafc', fontSize: '0.9rem', boxSizing: 'border-box', outline: 'none' }}
              />
            </div>

            <div style={{ marginBottom: '14px' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '5px', fontWeight: '600' }}>Content</label>
              <textarea
                value={createForm.content}
                onChange={(e) => setCreateForm({ ...createForm, content: e.target.value })}
                rows={6}
                placeholder="Prompt content..."
                style={{ width: '100%', padding: '9px 12px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.1)', backgroundColor: 'rgba(15,23,42,0.6)', color: '#f8fafc', fontSize: '0.9rem', boxSizing: 'border-box', outline: 'none', resize: 'vertical', fontFamily: 'inherit' }}
              />
            </div>

            <div style={{ marginBottom: '14px' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '5px', fontWeight: '600' }}>Variables (comma-separated)</label>
              <input
                type="text"
                value={createForm.variables}
                onChange={(e) => setCreateForm({ ...createForm, variables: e.target.value })}
                placeholder="e.g. name, topic"
                style={{ width: '100%', padding: '9px 12px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.1)', backgroundColor: 'rgba(15,23,42,0.6)', color: '#f8fafc', fontSize: '0.9rem', boxSizing: 'border-box', outline: 'none' }}
              />
            </div>

            <div style={{ marginBottom: '18px' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '5px', fontWeight: '600' }}>Author</label>
              <input
                type="text"
                value={createForm.author}
                onChange={(e) => setCreateForm({ ...createForm, author: e.target.value })}
                placeholder="Your name"
                style={{ width: '100%', padding: '9px 12px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.1)', backgroundColor: 'rgba(15,23,42,0.6)', color: '#f8fafc', fontSize: '0.9rem', boxSizing: 'border-box', outline: 'none' }}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button
                onClick={() => setShowCreateModal(false)}
                style={{ ...btnBase, backgroundColor: 'rgba(255,255,255,0.05)', color: '#94a3b8' }}
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={creating || !createForm.prompt_name.trim() || !createForm.content.trim()}
                style={{ ...btnBase, backgroundColor: '#3b82f6', color: '#fff', opacity: creating || !createForm.prompt_name.trim() || !createForm.content.trim() ? 0.5 : 1 }}
              >
                {creating ? 'Creating...' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}

      {viewingPrompt && (
        <div
          style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}
          onClick={(e) => { if (e.target === e.currentTarget) setViewingPrompt(null); }}
        >
          <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)', padding: '24px', width: '600px', maxHeight: '80vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '10px' }}>
              <h4 style={{ margin: 0, color: '#f8fafc', fontSize: '1.2rem' }}>
                View Prompt: {selectedPromptName} (v{viewingPrompt.version})
              </h4>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Author: {viewingPrompt.author}</span>
            </div>
            
            <div style={{ flex: 1, overflowY: 'auto', backgroundColor: 'rgba(15,23,42,0.6)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', marginBottom: '20px' }}>
              <pre style={{ margin: 0, color: '#f8fafc', whiteSpace: 'pre-wrap', wordBreak: 'break-word', fontFamily: 'monospace', fontSize: '0.85rem', lineHeight: '1.5' }}>
                {viewingPrompt.content}
              </pre>
            </div>
            
            {viewingPrompt.variables && viewingPrompt.variables.length > 0 && (
              <div style={{ marginBottom: '20px' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: '#94a3b8' }}>Variables: </span>
                {viewingPrompt.variables.map((v, i) => (
                  <span key={i} style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '4px', backgroundColor: 'rgba(59,130,246,0.15)', color: '#3b82f6', marginRight: '6px' }}>
                    {v}
                  </span>
                ))}
              </div>
            )}
            
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button
                onClick={() => {
                  handleCloneVersion(viewingPrompt);
                  setViewingPrompt(null);
                }}
                style={{ ...btnBase, backgroundColor: '#0284c7', color: '#fff' }}
              >
                ✍️ Edit Content
              </button>
              <button
                onClick={() => setViewingPrompt(null)}
                style={{ ...btnBase, backgroundColor: 'rgba(255,255,255,0.05)', color: '#94a3b8' }}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
