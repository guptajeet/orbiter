import React, { useState, useEffect, useRef } from 'react';
import { api } from '../utils/api';

export default function Settings() {
  const [settings, setSettings] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const [resumeFile, setResumeFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const [profileForm, setProfileForm] = useState({
    email_accounts: '',
    linkedin_url: '',
    indeed_url: '',
  });
  const [savingProfile, setSavingProfile] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [settingsData, profileData] = await Promise.allSettled([
        api.get('/api/settings'),
        api.get('/api/profile'),
      ]);
      if (settingsData.status === 'fulfilled') setSettings(settingsData.value);
      if (profileData.status === 'fulfilled') {
        const p = profileData.value;
        setProfile(p);
        setProfileForm({
          email_accounts: (p.email_accounts || []).join(', '),
          linkedin_url: p.linkedin_url || '',
          indeed_url: p.indeed_url || '',
        });
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateField = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
    setSaveSuccess(false);
  };

  const saveSettings = async () => {
    try {
      setSaving(true);
      setError(null);
      setSaveSuccess(false);
      await api.put('/api/settings', {
        automation_mode: settings.automation_mode,
        confidence_threshold: settings.confidence_threshold,
        auto_apply_enabled: settings.auto_apply_enabled,
        email_monitoring: settings.email_monitoring,
        job_discovery_interval: settings.job_discovery_interval,
        ai_providers: settings.ai_providers,
        job_sources: settings.job_sources
      });
      setSaveSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) return;
    try {
      setUploading(true);
      setError(null);
      setUploadResult(null);
      const result = await api.upload('/api/profile/resume', resumeFile);
      setUploadResult(result);
      setResumeFile(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && (file.name.endsWith('.pdf') || file.name.endsWith('.docx') || file.name.endsWith('.txt'))) {
      setResumeFile(file);
    }
  };

  const saveProfile = async () => {
    try {
      setSavingProfile(true);
      setError(null);
      setProfileSuccess(false);
      const emails = profileForm.email_accounts.split(',').map(e => e.trim()).filter(Boolean);
      await api.post('/api/profile', {
        email_accounts: emails,
        linkedin_url: profileForm.linkedin_url || null,
        indeed_url: profileForm.indeed_url || null,
        preferences: profile?.preferences || {},
        automation_config: profile?.automation_config || {},
      });
      setProfileSuccess(true);
      setTimeout(() => setProfileSuccess(false), 3000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingProfile(false);
    }
  };

  const inputStyle = {
    backgroundColor: '#0f172a',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    color: '#ffffff',
    padding: '8px 12px',
    borderRadius: '6px',
    width: '100%',
    fontSize: '0.9rem',
    boxSizing: 'border-box',
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div>
        <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>Mission Settings</h1>
        <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Upload your resume, set up your profile, and configure automation rules.</p>
      </div>

      {error && (
        <div style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#ef4444' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center', color: '#94a3b8' }}>Loading settings...</div>
      ) : (
        <>
          {/* Resume Upload */}
          <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
            <h3 style={{ margin: '0 0 5px 0', color: '#f8fafc' }}>Resume / CV</h3>
            <p style={{ margin: '0 0 20px 0', color: '#94a3b8', fontSize: '0.85rem' }}>
              Upload your resume so AI can score matches and tailor applications for you.
            </p>

            <div
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: dragOver ? '2px dashed #3b82f6' : '2px dashed rgba(255, 255, 255, 0.15)',
                borderRadius: '12px',
                padding: '40px 20px',
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: dragOver ? 'rgba(59, 130, 246, 0.05)' : 'rgba(15, 23, 42, 0.3)',
                transition: 'all 0.2s ease',
              }}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                style={{ display: 'none' }}
                onChange={(e) => { if (e.target.files[0]) setResumeFile(e.target.files[0]); }}
              />
              <div style={{ fontSize: '2rem', marginBottom: '10px' }}>📄</div>
              <div style={{ color: '#f8fafc', fontWeight: 'bold', marginBottom: '5px' }}>
                {resumeFile ? resumeFile.name : 'Drop your resume here or click to browse'}
              </div>
              <div style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                Supports PDF, DOCX, or TXT files
              </div>
            </div>

            {resumeFile && (
              <div style={{ marginTop: '15px', display: 'flex', alignItems: 'center', gap: '15px' }}>
                <span style={{ color: '#cbd5e1', fontSize: '0.9rem' }}>
                  Selected: <strong>{resumeFile.name}</strong> ({(resumeFile.size / 1024).toFixed(1)} KB)
                </span>
                <button
                  onClick={handleResumeUpload}
                  disabled={uploading}
                  style={{
                    backgroundColor: uploading ? '#475569' : '#3b82f6',
                    color: 'white',
                    fontWeight: 'bold',
                    padding: '8px 16px',
                    borderRadius: '6px',
                    border: 'none',
                    cursor: uploading ? 'not-allowed' : 'pointer',
                    fontSize: '0.85rem',
                  }}
                >
                  {uploading ? 'Uploading...' : 'Upload Resume'}
                </button>
                <button
                  onClick={() => setResumeFile(null)}
                  style={{
                    backgroundColor: 'transparent',
                    color: '#94a3b8',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    cursor: 'pointer',
                    fontSize: '0.85rem',
                  }}
                >
                  Cancel
                </button>
              </div>
            )}

            {uploadResult && (
              <div style={{
                marginTop: '15px',
                padding: '12px',
                borderRadius: '8px',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                border: '1px solid #10b981',
                color: '#10b981',
                fontSize: '0.9rem',
              }}>
                Resume uploaded successfully! Extracted {uploadResult.text_length} characters. AI parsing initiated in background.
              </div>
            )}
          </div>

          {/* User Profile */}
          <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
            <h3 style={{ margin: '0 0 5px 0', color: '#f8fafc' }}>Your Profile</h3>
            <p style={{ margin: '0 0 20px 0', color: '#94a3b8', fontSize: '0.85rem' }}>
              Link your job platform accounts so the system can auto-apply and track responses.
            </p>

            {profileSuccess && (
              <div style={{ padding: '10px', borderRadius: '8px', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', color: '#10b981', marginBottom: '15px', fontSize: '0.85rem' }}>
                Profile saved successfully.
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '6px', fontSize: '0.85rem' }}>
                  Email Addresses (comma-separated)
                </label>
                <input
                  type="text"
                  value={profileForm.email_accounts}
                  onChange={(e) => setProfileForm(prev => ({ ...prev, email_accounts: e.target.value }))}
                  placeholder="your.email@gmail.com, work@company.com"
                  style={inputStyle}
                />
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '6px', fontSize: '0.85rem' }}>
                    LinkedIn Profile URL
                  </label>
                  <input
                    type="url"
                    value={profileForm.linkedin_url}
                    onChange={(e) => setProfileForm(prev => ({ ...prev, linkedin_url: e.target.value }))}
                    placeholder="https://linkedin.com/in/yourname"
                    style={inputStyle}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '6px', fontSize: '0.85rem' }}>
                    Indeed Profile URL
                  </label>
                  <input
                    type="url"
                    value={profileForm.indeed_url}
                    onChange={(e) => setProfileForm(prev => ({ ...prev, indeed_url: e.target.value }))}
                    placeholder="https://indeed.com/in/yourname"
                    style={inputStyle}
                  />
                </div>
              </div>
              <button
                onClick={saveProfile}
                disabled={savingProfile}
                style={{
                  alignSelf: 'flex-start',
                  backgroundColor: savingProfile ? '#475569' : '#8b5cf6',
                  color: 'white',
                  fontWeight: 'bold',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  border: 'none',
                  cursor: savingProfile ? 'not-allowed' : 'pointer',
                  fontSize: '0.85rem',
                }}
              >
                {savingProfile ? 'Saving...' : 'Save Profile'}
              </button>
            </div>
          </div>

          {/* Workflow Rules + Provider Status */}
          <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '30px', alignItems: 'start' }}>
            <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
              <h3 style={{ margin: '0 0 20px 0', color: '#f8fafc' }}>Workflow Rules</h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '8px', fontSize: '0.9rem' }}>
                    Auto-Apply Similarity Threshold ({((settings?.confidence_threshold || 0.8) * 100).toFixed(0)}%)
                  </label>
                  <input
                    type="range"
                    min="0.5"
                    max="0.95"
                    step="0.05"
                    value={settings?.confidence_threshold || 0.8}
                    onChange={(e) => updateField('confidence_threshold', parseFloat(e.target.value))}
                    style={{ width: '100%', cursor: 'pointer' }}
                  />
                  <span style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '4px', display: 'block' }}>
                    Applications matching above this score bypass manual review in Autopilot mode.
                  </span>
                </div>

                <div>
                  <label style={{ display: 'block', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '8px', fontSize: '0.9rem' }}>
                    Automation Mode
                  </label>
                  <select
                    value={settings?.automation_mode || 'copilot'}
                    onChange={(e) => updateField('automation_mode', e.target.value)}
                    style={{ ...inputStyle, width: '200px' }}
                  >
                    <option value="advisor">Advisor</option>
                    <option value="copilot">Copilot</option>
                    <option value="autopilot">Autopilot</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontWeight: 'bold', color: '#cbd5e1', marginBottom: '8px', fontSize: '0.9rem' }}>
                    Job Discovery Interval (seconds)
                  </label>
                  <input
                    type="number"
                    value={settings?.job_discovery_interval || 3600}
                    onChange={(e) => updateField('job_discovery_interval', parseInt(e.target.value))}
                    style={{ ...inputStyle, width: '150px' }}
                  />
                  <span style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '4px', display: 'block' }}>
                    How often to scan for new job postings.
                  </span>
                </div>

                <div style={{ display: 'flex', gap: '20px' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: '#cbd5e1', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={settings?.auto_apply_enabled || false}
                      onChange={(e) => updateField('auto_apply_enabled', e.target.checked)}
                      style={{ width: '18px', height: '18px' }}
                    />
                    Auto-Apply Enabled
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: '#cbd5e1', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={settings?.email_monitoring || false}
                      onChange={(e) => updateField('email_monitoring', e.target.checked)}
                      style={{ width: '18px', height: '18px' }}
                    />
                    Email Monitoring
                  </label>
                </div>

                <button
                  onClick={saveSettings}
                  disabled={saving}
                  style={{
                    alignSelf: 'flex-start',
                    backgroundColor: saving ? '#475569' : '#3b82f6',
                    color: 'white',
                    fontWeight: 'bold',
                    padding: '10px 20px',
                    borderRadius: '8px',
                    border: 'none',
                    cursor: saving ? 'not-allowed' : 'pointer'
                  }}
                >
                  {saving ? 'Saving...' : 'Save Settings'}
                </button>
              </div>
            </div>

            <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
              <h3 style={{ margin: '0 0 15px 0', color: '#f8fafc' }}>Provider & Source Status</h3>

              {settings?.ai_providers && Object.keys(settings.ai_providers).length > 0 && (
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{ margin: '0 0 10px 0', color: '#cbd5e1', fontSize: '0.9rem' }}>AI Providers</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.85rem' }}>
                    {Object.entries(settings.ai_providers).map(([name, configured]) => (
                      <div key={name}>
                        {name}: <span style={{ color: configured ? '#10b981' : '#ef4444', fontWeight: 'bold' }}>
                          {configured ? 'Configured' : 'Missing'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {settings?.job_sources && Object.keys(settings.job_sources).length > 0 && (
                <div>
                  <h4 style={{ margin: '0 0 10px 0', color: '#cbd5e1', fontSize: '0.9rem' }}>Job Sources</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.85rem' }}>
                    {Object.entries(settings.job_sources).map(([name, configured]) => (
                      <div key={name}>
                        {name}: <span style={{ color: configured ? '#10b981' : '#ef4444', fontWeight: 'bold' }}>
                          {configured ? 'Configured' : 'Missing'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
