import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {
  const [activeService, setActiveService] = useState(null);

  const services = [
    {
      title: '⚠️ Abnormal Login Detection',
      description:
        'Detect unusual login attempts using AI-powered anomaly detection.',
    },
    {
      title: '🗃️ Unauthorized File Access Monitoring',
      description: 'Monitor and block unauthorized access to sensitive files.',
    },
    {
      title: '🤖 Fake & Bot Account Detection',
      description: 'Identify and stop bot or fake accounts in real time.',
    },
    {
      title: '🗒️ Smart Reporting Dashboard',
      description:
        'Get detailed reports and analytics in a centralized dashboard.',
    },
    {
      title: '⚡ Autonomous Response',
      description:
        'Automatically respond to threats and secure your system instantly.',
    },
  ];

  const styles = {
    page: { textAlign: 'center', fontFamily: 'Gill Sans, Calibri, sans-serif' },
    navbar: {
      display: 'flex',
      justifyContent: 'space-between',
      padding: '20px 60px',
      alignItems: 'center',
      color: '#f9f9f6',
      background: '#0f172a',
      boxShadow: '0 2px 5px #f9f9f6',
    },
    logo: { fontSize: '20px', fontWeight: 'bold' },
    navLinks: {
      listStyle: 'none',
      display: 'flex',
      gap: '20px',
      fontWeight: 500,
      cursor: 'pointer',
    },
    btn: {
      background: '#33335c',
      color: '#f9f8f8',
      border: 'none',
      padding: '10px 20px',
      borderRadius: '20px',
      cursor: 'pointer',
    },
    hero: {
      background: 'linear-gradient(90deg, #f6f9f9, #f6f9f9)',
      color: '#0f172a',
      padding: '100px 20px',
    },
    heroTitle: { fontSize: '48px', marginBottom: '20px' },
    heroText: { maxWidth: '600px', margin: 'auto', fontSize: '18px' },
    services: { padding: '60px 20px', background: '#0f172a', color: 'white' },
    serviceList: {
      display: 'flex',
      justifyContent: 'center',
      gap: '20px',
      margin: '30px 0',
      flexWrap: 'wrap',
    },
    service: {
      padding: '20px',
      border: '1px solid #06067d',
      borderRadius: '6px',
      background: 'white',
      color: '#070707',
      cursor: 'pointer',
      transition: '0.2s',
    },
    modalOverlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 999,
    },
    modal: {
      background: 'white',
      color: 'black',
      padding: '24px',
      borderRadius: '12px',
      width: '380px',
      maxWidth: '90%',
      textAlign: 'center',
    },
    closeBtn: {
      padding: '8px 16px',
      border: 'none',
      background: 'black',
      color: 'white',
      borderRadius: '6px',
      cursor: 'pointer',
    },
    pricing: {
      padding: '18px',
      textAlign: 'center',
      background: '#0f172a',
      color: 'white',
    },
    pricingCards: {
      display: 'flex',
      justifyContent: 'center',
      gap: '30px',
      flexWrap: 'wrap',
    },
    pricingCard: {
      background: 'white',
      color: '#333',
      borderRadius: '14px',
      padding: '30px 20px',
      width: '280px',
      boxShadow: '0 6px 15px rgba(0,0,0,0.15)',
      transition: '0.3s',
    },
    price: { fontSize: '28px', fontWeight: 'bold', marginBottom: '20px' },
    buyBtn: {
      background: 'linear-gradient(90deg, #1f14e6, #9333ea)',
      color: 'white',
      border: 'none',
      padding: '12px 20px',
      fontSize: '15px',
      fontWeight: 'bold',
      borderRadius: '25px',
      cursor: 'pointer',
    },
  };

  return (
    <div style={styles.page}>
      {/* Navbar */}
      <nav style={styles.navbar}>
        <div style={styles.logo}>NeuralGuardians</div>
        <ul style={styles.navLinks}>
          <li>Home</li>
          <li>About Us</li>
          <li>What We Do</li>
          <li>Pricing</li>
        </ul>
        <div style={{ display: 'flex', gap: '8px' }}>
          <Link to="/userlogin">
            <button style={styles.btn}>Test</button>
          </Link>

          <Link to="/adminlogin">
            <button style={styles.btn}>Admin</button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <header style={styles.hero}>
        <div>
          <h1 style={styles.heroTitle}>
            We build <br /> an Agentic-AI software
          </h1>
          <p style={styles.heroText}>
            We develop an Agentic AI-powered Smart Incident Responder that
            detects, analyzes, and responds to cyber threats in real time,
            protecting logins, files, and accounts with autonomous defense and
            clear reporting.
          </p>
        </div>
      </header>

      {/* What we do */}
      <section style={styles.services}>
        <h1>What we do?</h1>
        <div style={styles.serviceList}>
          {services.map((service, index) => (
            <div
              key={index}
              style={styles.service}
              onClick={() => setActiveService(service)}
            >
              {service.title}
            </div>
          ))}
        </div>

        {/* Modal Popup */}
        {activeService && (
          <div
            style={styles.modalOverlay}
            onClick={() => setActiveService(null)}
          >
            <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
              <h3>{activeService.title}</h3>
              <p>{activeService.description}</p>
              <button
                style={styles.closeBtn}
                onClick={() => setActiveService(null)}
              >
                Close
              </button>
            </div>
          </div>
        )}
      </section>

      {/* Pricing Section */}
      <section style={styles.pricing}>
        <h2>Pricing Table</h2>
        <div style={styles.pricingCards}>
          {/* Basic Plan */}
          <div style={styles.pricingCard}>
            <div
              style={{
                ...styles.pricingHeader,
                background: '#8b5cf6',
                color: 'white',
                padding: '8px',
                borderRadius: '10px',
              }}
            >
              Basic
            </div>
            <div style={styles.price}>$5</div>
            <ul style={{ textAlign: 'left' }}>
              <li>✔ Abnormal Login Detection (basic AI alerts)</li>
              <li>✔ Unauthorized File Access Alerts (up to 50 files)</li>
              <li>❌ Fake & Bot Account Detection</li>
              <li>❌ Automated Smart Reports</li>
              <li>✔ Notifications only</li>
              <li>❌ Autonomous Response</li>
            </ul>
            <button style={styles.buyBtn}>Buy Now</button>
          </div>

          {/* Standard Plan */}
          <div style={styles.pricingCard}>
            <div
              style={{
                ...styles.pricingHeader,
                background: '#3b82f6',
                color: 'white',
                padding: '8px',
                borderRadius: '10px',
              }}
            >
              Standard
            </div>
            <div style={styles.price}>$15</div>
            <ul style={{ textAlign: 'left' }}>
              <li>✔ Abnormal Login Detection (full)</li>
              <li>✔ Unauthorized File Access Monitoring (unlimited)</li>
              <li>❌ Fake & Bot Account Detection (manual flagging only)</li>
              <li>✔ Smart Reporting Dashboard (weekly reports)</li>
              <li>✔ Notifications</li>
              <li>❌ Autonomous Response</li>
            </ul>
            <button style={styles.buyBtn}>Buy Now</button>
          </div>

          {/* Premium Plan */}
          <div style={styles.pricingCard}>
            <div
              style={{
                ...styles.pricingHeader,
                background: '#f43f5e',
                color: 'white',
                padding: '8px',
                borderRadius: '10px',
              }}
            >
              Premium
            </div>
            <div style={styles.price}>$25</div>
            <ul style={{ textAlign: 'left' }}>
              <li>✔ Abnormal Login Detection (real-time AI)</li>
              <li>✔ Unauthorized File Access Monitoring (unlimited)</li>
              <li>✔ Fake & Bot Account Detection (real-time)</li>
              <li>✔ Smart Reporting Dashboard (custom reports)</li>
              <li>✔ Multi-channel Notifications (Email, SMS, Slack, Teams)</li>
              <li>✔ Autonomous Threat Response (auto-blocking threats)</li>
            </ul>
            <button style={styles.buyBtn}>Buy Now</button>
          </div>
        </div>
      </section>
    </div>
  );
}
