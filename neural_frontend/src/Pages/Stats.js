import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  // Threat overview stats
  const stats = [
    {
      id: 1,
      label: 'Active Threats',
      value: 23,
      change: '+5',
      color: '#ef4444',
      bg: '#2b1d21',
    },
    {
      id: 2,
      label: 'Blocked IPs',
      value: 1247,
      change: '+89',
      color: '#06b6d4',
      bg: '#1e2d3b',
    },
    {
      id: 3,
      label: 'Suspicious Users',
      value: 45,
      change: '-12',
      color: '#eab308',
      bg: '#2e2c1d',
    },

  ];

  // Pie chart data (security metrics)
  const pieData = [
    { name: 'Allowed', value: 70, color: '#22c55e' },
    { name: 'Blocked', value: 20, color: '#ef4444' },
    { name: 'Pending', value: 10, color: '#eab308' },
  ];

  // Weekly activity bar chart data
  const barData = [
    { name: 'Mon', allowed: 40, blocked: 20 },
    { name: 'Tue', allowed: 60, blocked: 30 },
    { name: 'Wed', allowed: 55, blocked: 25 },
    { name: 'Thu', allowed: 70, blocked: 40 },
    { name: 'Fri', allowed: 65, blocked: 35 },
    { name: 'Sat', allowed: 80, blocked: 45 },
    { name: 'Sun', allowed: 50, blocked: 30 },
  ];

  return (
    <div
      style={{
        background: '#0f172a',
        color: 'white',
        minHeight: '100vh',
        padding: '20px',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      {/* Header */}
      <header
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '30px',
        }}
      >
        <h2
          style={{
            fontSize: '24px',
            fontWeight: 'bold',
            background: 'linear-gradient(90deg, #f43f5e, #8b5cf6)',
            WebkitBackgroundClip: 'text',
            color: 'transparent',
          }}
        >
          NEURAL GUARDIANS
        </h2>
        <div style={{ display: 'flex', gap: '15px' }}>
          <Link to="/admindashboard" style={{ textDecoration: 'none' }}>
            <button
              style={{
                background: '#1e293b',
                padding: '8px 16px',
                borderRadius: '8px',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
              }}
            >
              Dashboard
            </button>
          </Link>

          <Link to="/stats" style={{ textDecoration: 'none' }}>
            <button
              style={{
                background: '#1e293b',
                padding: '8px 16px',
                borderRadius: '8px',
                border: 'none',
                color: '#38bdf8',
                cursor: 'pointer',
              }}
            >
              Stats
            </button>
          </Link>
        </div>
      </header>

      <p style={{ marginBottom: '20px', color: '#94a3b8' }}>
        Real-time Threat Monitoring & Response
      </p>

      <div
        style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}
      >
        {/* Left Side - Threat Overview */}
        <div>
          <h3 style={{ marginBottom: '10px' }}>Threat Overview</h3>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '20px',
            }}
          >
            {stats.map((stat) => (
              <div
                key={stat.id}
                style={{
                  background: stat.bg,
                  padding: '20px',
                  borderRadius: '12px',
                }}
              >
                <div
                  style={{
                    fontSize: '28px',
                    fontWeight: 'bold',
                    color: stat.color,
                  }}
                >
                  {stat.value}
                </div>
                <p style={{ margin: '5px 0', color: '#cbd5e1' }}>
                  {stat.label}
                </p>
                <small style={{ color: '#94a3b8' }}>{stat.change}</small>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side - Security Metrics */}
        <div>
          <h3 style={{ marginBottom: '10px' }}>Security Metrics</h3>

          {/* Pie Chart */}
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={pieData} dataKey="value" outerRadius={80} label>
                {pieData.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: 'none',
                  color: '#fff',
                }}
              />
            </PieChart>
          </ResponsiveContainer>

          {/* Weekly Activity Bar Chart */}
          <h4 style={{ marginTop: '20px' }}>Weekly Activity</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#cbd5e1" />
              <YAxis stroke="#cbd5e1" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: 'none',
                  color: '#fff',
                }}
              />
              <Bar dataKey="allowed" fill="#38bdf8" />
              <Bar dataKey="blocked" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
