import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import ConfidenceHeatmap from '../components/intelligence/ConfidenceHeatmap';

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [discovering, setDiscovering] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [jobDetail, setJobDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [applying, setApplying] = useState(false);
  const [applyResult, setApplyResult] = useState(null);

  const fetchJobs = () => {
    setLoading(true);
    api.get('/api/jobs')
      .then((data) => setJobs(data.jobs || []))
      .catch(() => setJobs([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchJobs(); }, []);

  useEffect(() => {
    if (selectedJob) {
      setLoadingDetail(true);
      setApplyResult(null);
      api.get(`/api/jobs/${selectedJob.id}`)
        .then(setJobDetail)
        .catch(() => setJobDetail(null))
        .finally(() => setLoadingDetail(false));
    }
  }, [selectedJob]);

  const handleDiscover = async () => {
    setDiscovering(true);
    try {
      await api.post('/api/jobs/discover');
      setTimeout(fetchJobs, 2000);
    } catch (e) {
      console.error('Discovery failed:', e);
    } finally {
      setDiscovering(false);
    }
  };

  const handleApply = async (jobId) => {
    setApplying(true);
    setApplyResult(null);
    try {
      const result = await api.post(`/api/jobs/${jobId}/apply`);
      setApplyResult({ success: true, message: `Application created for ${result.job_title} at ${result.company}` });
    } catch (e) {
      setApplyResult({ success: false, message: e.message || 'Failed to create application' });
    } finally {
      setApplying(false);
    }
  };

  const timeAgo = (iso) => {
    if (!iso) return '';
    try {
      const diff = Date.now() - new Date(iso).getTime();
      const mins = Math.floor(diff / 60000);
      if (mins < 1) return 'Just now';
      if (mins < 60) return `${mins}m ago`;
      const hrs = Math.floor(mins / 60);
      if (hrs < 24) return `${hrs}h ago`;
      return `${Math.floor(hrs / 24)}d ago`;
    } catch { return iso; }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>Jobs Explorer</h1>
          <p style={{ margin: '5px 0 0 0', color: '#94a3b8' }}>Search and explore opportunities ingested dynamically from APIs and RSS feeds.</p>
        </div>
        <button
          onClick={handleDiscover}
          disabled={discovering}
          style={{
            padding: '10px 20px',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: discovering ? '#334155' : '#3b82f6',
            color: '#f8fafc',
            fontWeight: 'bold',
            fontSize: '0.9rem',
            cursor: discovering ? 'not-allowed' : 'pointer',
            transition: 'background-color 0.15s',
          }}
          onMouseEnter={(e) => { if (!discovering) e.target.style.backgroundColor = '#2563eb'; }}
          onMouseLeave={(e) => { if (!discovering) e.target.style.backgroundColor = '#3b82f6'; }}
        >
          {discovering ? 'Discovering...' : 'Discover Jobs'}
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '30px', alignItems: 'start' }}>
        <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
          <h3 style={{ margin: '0 0 20px 0', color: '#f8fafc' }}>Ingested Job Feed ({jobs.length})</h3>
          {loading ? (
            <div style={{ color: '#94a3b8', padding: '20px', textAlign: 'center' }}>Loading jobs...</div>
          ) : jobs.length === 0 ? (
            <div style={{ color: '#94a3b8', padding: '40px 20px', textAlign: 'center' }}>
              No jobs discovered yet. Click "Discover Jobs" to fetch listings.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              {jobs.map((job) => (
                <div key={job.id} onClick={() => setSelectedJob(job)} style={{
                  padding: '16px',
                  borderRadius: '8px',
                  backgroundColor: selectedJob?.id === job.id ? 'rgba(59, 130, 246, 0.1)' : 'rgba(15, 23, 42, 0.4)',
                  border: selectedJob?.id === job.id ? '1px solid #3b82f6' : '1px solid rgba(255, 255, 255, 0.05)',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
                onMouseEnter={(e) => { if (selectedJob?.id !== job.id) e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.15)'; }}
                onMouseLeave={(e) => { if (selectedJob?.id !== job.id) e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.05)'; }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div style={{ flex: 1 }}>
                      <h4 style={{ margin: 0, color: '#f8fafc', fontSize: '1.05rem' }}>
                        {job.title}
                      </h4>
                      <div style={{ color: '#cbd5e1', fontSize: '0.85rem', marginTop: '4px' }}>
                        {job.company_name} • <span style={{ color: '#94a3b8' }}>{job.location}</span>
                      </div>
                      <div style={{ display: 'flex', gap: '8px', marginTop: '8px', flexWrap: 'wrap', fontSize: '0.75rem', color: '#94a3b8' }}>
                        <span style={{ padding: '2px 6px', backgroundColor: 'rgba(255, 255, 255, 0.05)', borderRadius: '4px' }}>Source: {job.source_name || job.source_type}</span>
                        {job.salary_range && <span style={{ padding: '2px 6px', backgroundColor: 'rgba(16, 185, 129, 0.1)', color: '#10b981', borderRadius: '4px' }}>{job.salary_range}</span>}
                        {job.first_seen_at && <span>{timeAgo(job.first_seen_at)}</span>}
                      </div>
                      {job.required_skills && job.required_skills.length > 0 && (
                        <div style={{ display: 'flex', gap: '5px', marginTop: '8px', flexWrap: 'wrap' }}>
                          {job.required_skills.slice(0, 5).map((skill, i) => (
                            <span key={i} style={{ padding: '2px 6px', backgroundColor: 'rgba(139, 92, 246, 0.15)', color: '#a78bfa', borderRadius: '4px', fontSize: '0.7rem' }}>{skill}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Job Detail Panel */}
          {selectedJob && (
            <div className="glass-panel" style={{ backgroundColor: 'rgba(30, 41, 59, 0.7)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '15px' }}>
                <h3 style={{ margin: 0, color: '#f8fafc', fontSize: '1.1rem' }}>{jobDetail?.title || selectedJob.title}</h3>
                <button onClick={() => { setSelectedJob(null); setJobDetail(null); }} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', fontSize: '1.2rem' }}>✕</button>
              </div>

              {loadingDetail ? (
                <div style={{ color: '#94a3b8', padding: '20px', textAlign: 'center' }}>Loading details...</div>
              ) : jobDetail ? (
                <div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '15px' }}>
                    <div style={{ fontSize: '0.9rem', color: '#cbd5e1' }}>
                      <strong>{jobDetail.company_name}</strong> • {jobDetail.location}
                    </div>
                    {jobDetail.salary_range && (
                      <div style={{ fontSize: '0.85rem', color: '#10b981' }}>{jobDetail.salary_range}</div>
                    )}
                    {jobDetail.url && (
                      <a href={jobDetail.url} target="_blank" rel="noopener noreferrer" style={{ color: '#60a5fa', fontSize: '0.85rem', textDecoration: 'none' }}>
                        View Original Posting ↗
                      </a>
                    )}
                  </div>

                  {jobDetail.description_clean && (
                    <div style={{ marginBottom: '15px' }}>
                      <h4 style={{ margin: '0 0 8px 0', color: '#cbd5e1', fontSize: '0.9rem' }}>Description</h4>
                      <div style={{ fontSize: '0.8rem', color: '#94a3b8', lineHeight: '1.5', maxHeight: '200px', overflow: 'auto', padding: '10px', backgroundColor: 'rgba(15, 23, 42, 0.3)', borderRadius: '6px' }}>
                        {jobDetail.description_clean}
                      </div>
                    </div>
                  )}

                  {jobDetail.required_skills && jobDetail.required_skills.length > 0 && (
                    <div style={{ marginBottom: '15px' }}>
                      <h4 style={{ margin: '0 0 8px 0', color: '#cbd5e1', fontSize: '0.9rem' }}>Required Skills</h4>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {jobDetail.required_skills.map((skill, i) => (
                          <span key={i} style={{ padding: '4px 8px', backgroundColor: 'rgba(139, 92, 246, 0.15)', color: '#a78bfa', borderRadius: '4px', fontSize: '0.8rem' }}>{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {jobDetail.industry_tags && jobDetail.industry_tags.length > 0 && (
                    <div>
                      <h4 style={{ margin: '0 0 8px 0', color: '#cbd5e1', fontSize: '0.9rem' }}>Industry</h4>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {jobDetail.industry_tags.map((tag, i) => (
                          <span key={i} style={{ padding: '4px 8px', backgroundColor: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', borderRadius: '4px', fontSize: '0.8rem' }}>{tag}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {applyResult && (
                    <div style={{
                      marginTop: '15px',
                      padding: '10px 14px',
                      borderRadius: '8px',
                      backgroundColor: applyResult.success ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                      border: `1px solid ${applyResult.success ? '#10b981' : '#ef4444'}`,
                      color: applyResult.success ? '#10b981' : '#ef4444',
                      fontSize: '0.85rem',
                    }}>
                      {applyResult.message}
                    </div>
                  )}

                  <button
                    onClick={() => handleApply(jobDetail.id)}
                    disabled={applying}
                    style={{
                      marginTop: '15px',
                      width: '100%',
                      padding: '10px',
                      borderRadius: '8px',
                      border: 'none',
                      backgroundColor: applying ? '#334155' : '#10b981',
                      color: '#ffffff',
                      fontWeight: 'bold',
                      fontSize: '0.9rem',
                      cursor: applying ? 'not-allowed' : 'pointer',
                      transition: 'background-color 0.15s',
                    }}
                  >
                    {applying ? 'Creating Application...' : 'Apply to This Job'}
                  </button>
                </div>
              ) : (
                <div style={{ color: '#94a3b8', padding: '20px', textAlign: 'center' }}>Could not load details.</div>
              )}
            </div>
          )}

          <ConfidenceHeatmap />
        </div>
      </div>
    </div>
  );
}
