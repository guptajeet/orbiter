import React from 'react';
import { useNavigate } from 'react-router-dom';

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#0f172a',
    color: '#f8fafc',
    padding: '32px',
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
  },
  header: {
    textAlign: 'center',
    marginBottom: '48px',
  },
  title: {
    fontSize: '36px',
    fontWeight: 700,
    marginBottom: '12px',
    background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  subtitle: {
    fontSize: '16px',
    color: '#94a3b8',
    maxWidth: '600px',
    margin: '0 auto',
    lineHeight: 1.6,
  },
  grid: {
    maxWidth: '900px',
    margin: '0 auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '24px',
  },
  card: {
    backgroundColor: '#1e293b',
    borderRadius: '16px',
    border: '1px solid rgba(148, 163, 184, 0.1)',
    padding: '32px',
    backdropFilter: 'blur(12px)',
  },
  stepLabel: {
    fontSize: '12px',
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '1.5px',
    marginBottom: '8px',
  },
  cardTitle: {
    fontSize: '22px',
    fontWeight: 600,
    color: '#f8fafc',
    marginBottom: '12px',
  },
  description: {
    fontSize: '14px',
    color: '#94a3b8',
    lineHeight: 1.7,
    marginBottom: '20px',
  },
  stepsList: {
    listStyle: 'none',
    padding: 0,
    margin: '0 0 24px 0',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  stepItem: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    fontSize: '14px',
    color: '#cbd5e1',
    lineHeight: 1.6,
  },
  bullet: {
    width: '6px',
    height: '6px',
    minWidth: '6px',
    borderRadius: '50%',
    marginTop: '7px',
  },
  badge: {
    display: 'inline-block',
    padding: '2px 8px',
    borderRadius: '6px',
    fontSize: '11px',
    fontWeight: 600,
    marginLeft: '6px',
  },
  btn: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 20px',
    borderRadius: '10px',
    border: 'none',
    fontSize: '14px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  btnPrimary: {
    backgroundColor: '#3b82f6',
    color: '#ffffff',
  },
  btnGreen: {
    backgroundColor: '#10b981',
    color: '#ffffff',
  },
  btnPurple: {
    backgroundColor: '#8b5cf6',
    color: '#ffffff',
  },
  btnAmber: {
    backgroundColor: '#f59e0b',
    color: '#0f172a',
  },
  tipBox: {
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    border: '1px solid rgba(59, 130, 246, 0.25)',
    borderRadius: '10px',
    padding: '16px 20px',
    marginTop: '16px',
  },
  tipTitle: {
    fontSize: '13px',
    fontWeight: 600,
    color: '#3b82f6',
    marginBottom: '6px',
  },
  tipText: {
    fontSize: '13px',
    color: '#94a3b8',
    lineHeight: 1.6,
  },
  divider: {
    height: '1px',
    backgroundColor: 'rgba(148, 163, 184, 0.1)',
    margin: '16px 0',
  },
  troubleshootingItem: {
    backgroundColor: 'rgba(15, 23, 42, 0.5)',
    borderRadius: '8px',
    padding: '14px 18px',
    marginBottom: '10px',
  },
  troubleshootingQ: {
    fontSize: '14px',
    fontWeight: 600,
    color: '#f8fafc',
    marginBottom: '4px',
  },
  troubleshootingA: {
    fontSize: '13px',
    color: '#94a3b8',
    lineHeight: 1.6,
  },
};

export default function QuickStartGuide() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Quick Start Guide</h1>
        <p style={styles.subtitle}>
          Everything you need to know to get up and running with Orbiter.
          Follow these steps to automate your job search with AI.
        </p>
      </div>

      <div style={styles.grid}>
        <div style={{ ...styles.card, borderLeft: '3px solid #3b82f6' }}>
          <div style={{ ...styles.stepLabel, color: '#3b82f6' }}>Welcome</div>
          <h2 style={styles.cardTitle}>What is Orbiter?</h2>
          <p style={styles.description}>
            Orbiter is an AI-powered job search automation platform. It discovers jobs from
            multiple sources, matches them to your skills, crafts tailored applications, manages
            recruiter relationships, and tracks your entire pipeline — all so you can focus on
            what matters: landing the right role.
          </p>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #8b5cf6' }}>
          <div style={{ ...styles.stepLabel, color: '#8b5cf6' }}>Step 1</div>
          <h2 style={styles.cardTitle}>Set Up Your Profile</h2>
          <p style={styles.description}>
            Your profile is the foundation. The AI uses it to match jobs and tailor every application.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#8b5cf6' }} />
              <span>Navigate to the <strong>Settings</strong> page from the sidebar.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#8b5cf6' }} />
              <span>Upload your resume in PDF, DOCX, or TXT format.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#8b5cf6' }} />
              <span>Fill in your email addresses, LinkedIn URL, and Indeed URL.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#8b5cf6' }} />
              <span>The AI will automatically parse your skills, experience, and preferences.</span>
            </li>
          </ul>
          <button style={{ ...styles.btn, ...styles.btnPurple }} onClick={() => navigate('/settings')}>
            Go to Settings
          </button>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #10b981' }}>
          <div style={{ ...styles.stepLabel, color: '#10b981' }}>Step 2</div>
          <h2 style={styles.cardTitle}>Configure Automation Settings</h2>
          <p style={styles.description}>
            Fine-tune how Orbiter works for you. You control the level of automation.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>
                <strong>Confidence Threshold</strong> — Set how confident the AI must be before
                auto-applying. Higher = fewer but better matches.
              </span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>
                <strong>Automation Mode</strong> — Choose your comfort level:
                <span style={{ ...styles.badge, backgroundColor: 'rgba(59,130,246,0.15)', color: '#3b82f6' }}>Advisor</span>
                <span style={{ ...styles.badge, backgroundColor: 'rgba(139,92,246,0.15)', color: '#8b5cf6' }}>Copilot</span>
                <span style={{ ...styles.badge, backgroundColor: 'rgba(16,185,129,0.15)', color: '#10b981' }}>Autopilot</span>
              </span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>Toggle auto-apply and email monitoring on or off.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>Set the job discovery interval to control how often new jobs are fetched.</span>
            </li>
          </ul>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button style={{ ...styles.btn, ...styles.btnPrimary }} onClick={() => navigate('/settings')}>
              Configure Settings
            </button>
            <button style={{ ...styles.btn, ...styles.btnGreen }} onClick={() => navigate('/operations')}>
              View Modes
            </button>
          </div>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #3b82f6' }}>
          <div style={{ ...styles.stepLabel, color: '#3b82f6' }}>Step 3</div>
          <h2 style={styles.cardTitle}>Discover Jobs</h2>
          <p style={styles.description}>
            Orbiter pulls opportunities from multiple sources and ranks them by match quality.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#3b82f6' }} />
              <span>Go to <strong>Jobs Explorer</strong> from the sidebar.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#3b82f6' }} />
              <span>Click <strong>"Discover Jobs"</strong> to fetch the latest listings.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#3b82f6' }} />
              <span>
                Jobs are sourced from
                <span style={{ ...styles.badge, backgroundColor: 'rgba(59,130,246,0.15)', color: '#3b82f6' }}>Remotive</span>
                <span style={{ ...styles.badge, backgroundColor: 'rgba(139,92,246,0.15)', color: '#8b5cf6' }}>Adzuna</span>
                <span style={{ ...styles.badge, backgroundColor: 'rgba(16,185,129,0.15)', color: '#10b981' }}>JSearch</span>
                <span style={{ ...styles.badge, backgroundColor: 'rgba(245,158,11,0.15)', color: '#f59e0b' }}>RSS Feeds</span>
              </span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#3b82f6' }} />
              <span>Click any job card to see full details, skills match percentage, and tags.</span>
            </li>
          </ul>
          <button style={{ ...styles.btn, ...styles.btnPrimary }} onClick={() => navigate('/jobs')}>
            Open Jobs Explorer
          </button>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #f59e0b' }}>
          <div style={{ ...styles.stepLabel, color: '#f59e0b' }}>Step 4</div>
          <h2 style={styles.cardTitle}>Review & Apply</h2>
          <p style={styles.description}>
            Track every application through its lifecycle and control what gets submitted.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#f59e0b' }} />
              <span>Navigate to the <strong>Applications</strong> board.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#f59e0b' }} />
              <span>
                In Advisor or Copilot mode, AI-matched jobs appear in the
                <strong> "Review Needed"</strong> column.
              </span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#f59e0b' }} />
              <span>Click <strong>Approve</strong> to submit an application, or <strong>Reject</strong> to skip.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#f59e0b' }} />
              <span>Track applications through <strong>Interview</strong>, <strong>Offer</strong>, and <strong>Rejected</strong> stages.</span>
            </li>
          </ul>
          <button style={{ ...styles.btn, ...styles.btnAmber }} onClick={() => navigate('/applications')}>
            Open Applications Board
          </button>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #10b981' }}>
          <div style={{ ...styles.stepLabel, color: '#10b981' }}>Step 5</div>
          <h2 style={styles.cardTitle}>Manage Recruiter Relationships</h2>
          <p style={styles.description}>
            Keep track of every recruiter interaction so you never miss a follow-up.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>Go to <strong>Recruiter CRM</strong> from the sidebar.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>Add recruiter contacts manually — they are also auto-added from your email.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#10b981' }} />
              <span>View relationship scores, conversation history, and follow-up schedules at a glance.</span>
            </li>
          </ul>
          <button style={{ ...styles.btn, ...styles.btnGreen }} onClick={() => navigate('/crm')}>
            Open Recruiter CRM
          </button>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #8b5cf6' }}>
          <div style={{ ...styles.stepLabel, color: '#8b5cf6' }}>Step 6</div>
          <h2 style={styles.cardTitle}>Monitor Analytics</h2>
          <p style={styles.description}>
            Understand your performance and optimize your strategy with data.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#8b5cf6' }} />
              <span>Go to <strong>Analytics & Eval</strong> to view match precision, callback rate, and email response rate.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#8b5cf6' }} />
              <span>Use the <strong>PromptOps</strong> console to manage and compare prompt versions for application quality.</span>
            </li>
          </ul>
          <button style={{ ...styles.btn, ...styles.btnPurple }} onClick={() => navigate('/analytics')}>
            Open Analytics
          </button>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #94a3b8' }}>
          <div style={{ ...styles.stepLabel, color: '#94a3b8' }}>Step 7 — Advanced</div>
          <h2 style={styles.cardTitle}>System Operations</h2>
          <p style={styles.description}>
            For advanced users who want full control over automation behavior and system health.
          </p>
          <ul style={styles.stepsList}>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#94a3b8' }} />
              <span>Go to <strong>Operations</strong> to switch between automation modes in real time.</span>
            </li>
            <li style={styles.stepItem}>
              <span style={{ ...styles.bullet, backgroundColor: '#94a3b8' }} />
              <span>Run chaos and resilience tests to verify system stability under stress.</span>
            </li>
          </ul>
          <button style={{ ...styles.btn, backgroundColor: '#334155', color: '#f8fafc' }} onClick={() => navigate('/operations')}>
            Open Operations
          </button>
        </div>

        <div style={{ ...styles.card, borderLeft: '3px solid #3b82f6' }}>
          <div style={{ ...styles.stepLabel, color: '#3b82f6' }}>Tips & Troubleshooting</div>
          <h2 style={styles.cardTitle}>Need Help?</h2>

          <div style={styles.troubleshootingItem}>
            <div style={styles.troubleshootingQ}>No jobs are appearing after discovery</div>
            <div style={styles.troubleshootingA}>
              Make sure your profile is complete and your confidence threshold isn't set too high.
              Try lowering it to 0.5 and re-running discovery.
            </div>
          </div>

          <div style={styles.troubleshootingItem}>
            <div style={styles.troubleshootingQ}>Applications aren't being submitted</div>
            <div style={styles.troubleshootingA}>
              Check that auto-apply is toggled on in Settings and that your email accounts are connected.
              In Copilot or Advisor mode, you need to manually approve each application.
            </div>
          </div>

          <div style={styles.troubleshootingItem}>
            <div style={styles.troubleshootingQ}>Skills match seems inaccurate</div>
            <div style={styles.troubleshootingA}>
              Re-upload a more detailed resume or manually edit your skills in Settings.
              The AI refines its understanding as you approve or reject more matches.
            </div>
          </div>

          <div style={styles.troubleshootingItem}>
            <div style={styles.troubleshootingQ}>Email monitoring isn't picking up recruiter replies</div>
            <div style={styles.troubleshootingA}>
              Verify your email is connected in Settings and that IMAP access is enabled for your provider.
              Check the Operations page for email service health.
            </div>
          </div>

          <div style={styles.troubleshootingItem}>
            <div style={styles.troubleshootingQ}>Where do I get support?</div>
            <div style={styles.troubleshootingA}>
              Visit the Operations page to check system status. For bugs or feature requests,
              open an issue on the Orbiter GitHub repository.
            </div>
          </div>

          <div style={styles.divider} />

          <div style={styles.tipBox}>
            <div style={styles.tipTitle}>Pro Tip</div>
            <div style={styles.tipText}>
              Start with <strong>Copilot mode</strong> to see what the AI recommends before letting it
              apply on its own. This helps you calibrate your confidence threshold and understand
              the match quality.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
