
import { FaMapMarkerAlt, FaClock, FaDollarSign } from 'react-icons/fa';
import { FiEye, FiX } from 'react-icons/fi';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function MonitoringDashboard() {
      const [suspiciousLogins, setSuspiciousLogins] = useState([]);
      const [botDetections, setBotDetections] = useState([]);
      const [unauthorizedActivity, setUnauthorizedActivity] = useState([]);
      const [incidentReports, setIncidentReports] = useState([]);

    useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // ✅ Fetch Unauthorized Activity
        const uaRes = await fetch("http://localhost:8000/file-access");
        const uaData = await uaRes.json();
        setUnauthorizedActivity(uaData);

        // ✅ Fetch Suspicious Logins
        const loginRes = await fetch('http://127.0.0.1:8000/failed-logins');
        const loginData = await loginRes.json();
        setSuspiciousLogins(loginData);

        // ✅ Fetch Bot Detections
        
    setBotDetections([
       {
         name: 'bot_detection_001',
         tag: 'AUTO-BLOCKED',
         pattern: 'Rapid API Calls',
         confidence: '98%',
         requests: '2,847/min',
         seen: '14:32:15',
       },
       {
         name: 'sus_account_042',
         tag: 'FLAGGED',
         pattern: 'Fake Profile Data',
         confidence: '87%',
         requests: '1/sec',
         seen: '14:28:33',
       },
       {
         name: 'crawler_x23n',
         tag: 'RATE-LIMITED',
         pattern: 'Scraping Behavior',
         confidence: '72%',
         requests: '450/min',
         seen: '14:25:10',
       },
     ]);
        // ✅ Fetch Incident Reports
        const incidentRes = await fetch("http://localhost:8000/incidents");
        const incidentData = await incidentRes.json();
        setIncidentReports(incidentData);
      } catch (err) {
        console.error("Error fetching dashboard data:", err);
      }
    };

    fetchDashboardData();

    // optional refresh
    const interval = setInterval(fetchDashboardData, 60000);
    return () => clearInterval(interval);
  }, []);

  const styles = {
    wrapper: {
      maxWidth: 2000,
      margin: '0 auto',
      padding: 20,
      backgroundColor: '#0d1117',
      color: '#fff',
      fontFamily: '"Segoe UI", sans-serif',
    },
    navbar: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingBottom: 20,
      borderBottom: '1px solid #2d3748',
    },
    logo: { fontSize: 22, fontWeight: 'bold' },
    logoCyan: { color: '#22d3ee' },
    logoPurple: { color: '#a78bfa' },
    navButtons: { display: 'flex', gap: 12 },
    btn: {
      background: 'rgba(17, 24, 39, 0.85)',
      border: 'none',
      padding: '8px 18px',
      borderRadius: 8,
      color: '#d1d5db',
      cursor: 'pointer',
    },
    btnActive: { background: '#2563eb', color: '#fff' },
    contentGrid: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 20,
      marginBottom: 25,
    },
    card: {
      backgroundColor: '#1a2234',
      borderRadius: 12,
      padding: 15,
      boxShadow: '0px 4px 15px rgba(0,0,0,0.5)',
    },
    cardHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      fontSize: 14,
      color: '#d1d5db',
      textTransform: 'uppercase',
      marginBottom: 10,
    },
    badge: {
      fontSize: 11,
      fontWeight: 'bold',
      padding: '2px 6px',
      borderRadius: 6,
    },
    badgeRed: { background: '#ef4444' },
    badgePurple: { background: '#a78bfa' },
    badgeOrange: { background: '#f97316' },
    badgeBlue: { background: '#3b82f6' },
    list: { listStyle: 'none', padding: 0, margin: 0 },
    listItem: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      padding: 12,
      borderBottom: '1px solid #2d3748',
    },
    listLeft: { maxWidth: '65%' },
    user: { fontWeight: 'bold', margin: '0 0 5px' },
    meta: { fontSize: 12, color: '#9ca3af', margin: '2px 0' },
    reason: { fontSize: 12, color: '#9ca3af', margin: '2px 0' },
    highlight: { color: '#22d3ee' },
    status: {
      fontSize: 11,
      fontWeight: 'bold',
      marginLeft: 6,
      padding: '2px 6px',
      borderRadius: 5,
    },
    statusBlocked: { background: '#ef4444' },
    statusFlagged: { background: '#f59e0b' },
    statusMonitoring: { background: '#3b82f6' },
    statusAutoBlocked: { background: '#ef4444' },
    statusRateLimited: { background: '#facc15' },
    statusHigh: { background: '#ef4444' },
    statusMedium: { background: '#f59e0b' },
    statusCritical: { background: '#b91c1c' },
    statusInvestigating: { background: '#3b82f6' },
    statusResolved: { background: '#10b981' },
    statusOngoing: { background: '#f59e0b' },
    actions: { display: 'flex', gap: 6 },
    actionBtn: {
      border: 'none',
      padding: 6,
      borderRadius: 6,
      cursor: 'pointer',
      fontSize: 14,
    },
    actionBtnGreen: { background: '#10b981', color: '#fff' },
    actionBtnRed: { background: '#ef4444', color: '#fff' },
  };

  const getStatusStyle = (status) => {
    if (!status || typeof status !== 'string') return {}; // 🛡 prevent crash
    switch (status.toLowerCase()) {
      case 'blocked':
        return styles.statusBlocked;
      case 'flagged':
        return styles.statusFlagged;
      case 'monitoring':
        return styles.statusMonitoring;
      case 'auto-blocked':
        return styles.statusAutoBlocked;
      case 'rate-limited':
        return styles.statusRateLimited;
      case 'high':
        return styles.statusHigh;
      case 'medium':
        return styles.statusMedium;
      case 'critical':
        return styles.statusCritical;
      case 'investigating':
        return styles.statusInvestigating;
      case 'resolved':
        return styles.statusResolved;
      case 'ongoing':
        return styles.statusOngoing;
      default:
        return {};
    }
  };


  return (
    <div style={styles.wrapper}>
      {/* Navbar */}
      <header style={styles.navbar}>
        <h1 style={styles.logo}>
          <span style={styles.logoCyan}>NEURAL</span>{' '}
          <span style={styles.logoPurple}>GUARDIANS</span>
        </h1>
        <div style={styles.navButtons}>
          <button style={styles.btn}>
            <Link
              to="/admindashboard"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              Dashboard
            </Link>
          </button>

          <button style={{ ...styles.btn, ...styles.btnActive }}>
            <Link
              to="/stats"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              Stats
            </Link>
          </button>
        </div>
      </header>

      {/* Suspicious Logins + Bot Detection */}
      <div style={styles.contentGrid}>
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <span>SUSPICIOUS LOGINS</span>
            <span style={{ ...styles.badge, ...styles.badgeRed }}>
              4 ACTIVE
            </span>
          </div>
          <ul style={styles.list}>
            {suspiciousLogins.map((item, idx) => (
              <li key={idx} style={styles.listItem}>
                <div style={styles.listLeft}>
                  <p style={styles.user}>
                    {item.user}{' '}
                    <span
                      style={{
                        ...styles.status,
                        ...getStatusStyle(item.status),
                      }}
                    >
                      {item.status}
                    </span>{' '}
                    RISK: {item.risk}
                  </p>
                  <p style={styles.meta}>
                    <FaMapMarkerAlt /> {item.location}
                  </p>
                  <p style={styles.reason}>Reason: {item.reason}</p>
                </div>
                <div>
                  <p style={styles.meta}>
                    <FaClock /> {item.time}
                  </p>
                  <div style={styles.actions}>
                    <button
                      style={{ ...styles.actionBtn, ...styles.actionBtnGreen }}
                    >
                      <FiEye />
                    </button>
                    <button
                      style={{ ...styles.actionBtn, ...styles.actionBtnRed }}
                    >
                      <FiX />
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <span>BOT DETECTION</span>
            <span style={{ ...styles.badge, ...styles.badgePurple }}>
              4 DETECTED
            </span>
          </div>
          <ul style={styles.list}>
            {botDetections.map((bot, idx) => (
              <li key={idx} style={styles.listItem}>
                <div style={styles.listLeft}>
                  <p style={styles.user}>
                    {bot.name}{' '}
                    <span
                      style={{ ...styles.status, ...getStatusStyle(bot.tag) }}
                    >
                      {bot.tag}
                    </span>
                  </p>
                  <p style={styles.reason}>Pattern: {bot.pattern}</p>
                  <p style={styles.meta}>
                    Confidence:{' '}
                    <span style={styles.highlight}>{bot.confidence}</span>
                  </p>
                </div>
                <div>
                  <p style={styles.meta}>Requests: {bot.requests}</p>
                  <p style={styles.meta}>First Seen: {bot.seen}</p>
                  <div style={styles.actions}>
                    <button
                      style={{ ...styles.actionBtn, ...styles.actionBtnGreen }}
                    >
                      <FiEye />
                    </button>
                    <button
                      style={{ ...styles.actionBtn, ...styles.actionBtnRed }}
                    >
                      <FiX />
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Unauthorized Activity + Incident Reports */}
      <div style={styles.contentGrid}>
        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <span>UNAUTHORIZED ACTIVITY</span>
            <span style={{ ...styles.badge, ...styles.badgeOrange }}>
              4 INCIDENTS
            </span>
          </div>
          <ul style={styles.list}>
            {unauthorizedActivity.map((act, idx) => (
              <li key={idx} style={styles.listItem}>
                <div style={styles.listLeft}>
                  <p style={styles.user}>
                    <FaDollarSign /> {act.user}
                  </p>
                  <p style={styles.reason}>{act.action}</p>
                </div>
                <div>
                  <span
                    style={{
                      ...styles.status,
                      ...getStatusStyle(act.severity),
                    }}
                  >
                    {act.severity}
                  </span>
                  <span
                    style={{ ...styles.status, ...getStatusStyle(act.status) }}
                  >
                    {act.status}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div style={styles.card}>
          <div style={styles.cardHeader}>
            <span>INCIDENT REPORTS</span>
            <span style={{ ...styles.badge, ...styles.badgeBlue }}>
              {incidentReports.length} REPORTS
            </span>
          </div>
          <ul style={styles.list}>
            {incidentReports.map((rep, idx) => (
              <li key={idx} style={styles.listItem}>
                <div style={styles.listLeft}>
                  <p style={styles.user}>
                    User: {rep.username || rep.event?.username}
                  </p>
                  <p style={styles.reason}>File: {rep.event?.file_path}</p>
                  <p style={styles.reason}>Action: {rep.action?.action}</p>
                  <p style={styles.reason}>Reason: {rep.risk?.explanation}</p>
                  <p style={styles.reason}>Report: {rep.report}</p>
                </div>
                <div>
                  <span
                    style={{
                      ...styles.status,
                      ...getStatusStyle(rep.risk?.risk),
                    }}
                  >
                    {rep.risk?.risk?.toUpperCase()}
                  </span>
                  <span
                    style={{
                      ...styles.status,
                      ...getStatusStyle(
                        rep.action?.action === 'block_user'
                          ? 'blocked'
                          : 'allowed'
                      ),
                    }}
                  >
                    {rep.action?.action === 'block_user'
                      ? 'BLOCKED'
                      : 'ALLOWED'}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
