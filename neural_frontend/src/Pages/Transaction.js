import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { FaArrowDown, FaArrowUp, FaExchangeAlt } from 'react-icons/fa';
import { Link, useLocation } from 'react-router-dom';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import Swal from 'sweetalert2';
import { useNavigate } from 'react-router-dom';

import './Transaction.css';

const priceData = [
  { time: '00:00', price: 44000 },
  { time: '04:00', price: 44500 },
  { time: '08:00', price: 44200 },
  { time: '12:00', price: 44600 },
  { time: '16:00', price: 44800 },
  { time: '20:00', price: 44750 },
  { time: '24:00', price: 44850 },
];

const transactions = [
  {
    id: 1,
    icon: <FaArrowDown className="tx-icon buy" />,
    type: 'Buy BTC',
    amount: '0.0543 BTC',
    value: '$2,328.45',
    time: '2 hours ago',
    status: 'Completed',
  },
  {
    id: 2,
    icon: <FaArrowUp className="tx-icon sell" />,
    type: 'Sell ETH',
    amount: '1.2456 ETH',
    value: '$3,298.76',
    time: '5 hours ago',
    status: 'Completed',
  },
  {
    id: 3,
    icon: <FaExchangeAlt className="tx-icon transfer" />,
    type: 'Transfer USDC',
    amount: '5000.00 USDC',
    value: '$5,000.00',
    time: '1 day ago',
    status: 'Pending',
  },
  {
    id: 4,
    icon: <FaArrowDown className="tx-icon buy" />,
    type: 'Buy SOL',
    amount: '45.67 SOL',
    value: '$4,498.23',
    time: '2 days ago',
    status: 'Completed',
  },
];

export default function BitcoinSection() {
  // ✅ accept username prop
  // Function to generate PDF report + send POST to /incident
    const location = useLocation();
    const username = location.state?.username || 'guest';
   const navigate = useNavigate();
  const generateReport = async (tx) => {
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text('Transaction Report', 14, 22);

    doc.setFontSize(12);
    doc.text(`Transaction ID: ${tx.id}`, 14, 35);

    autoTable(doc, {
      startY: 45,
      head: [['Field', 'Value']],
      body: [
        ['Type', tx.type],
        ['Amount', tx.amount],
        ['Value', tx.value],
        ['Time', tx.time],
        ['Status', tx.status],
      ],
    });

    // ✅ Filename + file path
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `transaction_${tx.id}.pdf`;
    const filePath = `/reports/${filename}-${timestamp}`;

    // Save locally
    doc.save(filename);

    // ✅ Incident payload
    const incidentPayload = {
      username: username || 'unknown', // ✅ from prop
      file_path: filePath,
      type: 'file_access',
      timestamp: new Date().toISOString(),
    };

    try {
      const res = await fetch('http://localhost:8000/incident', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(incidentPayload),
      });

      const data = await res.json();
      console.log('Incident logged:', data);

      // ✅ Check backend response
      if (data?.action?.action === 'block_user') {
        // Clear localStorage
        localStorage.clear();

        // Popup with SweetAlert
        Swal.fire({
          icon: 'error',
          title: 'Access Blocked',
          text:
            data.action.details.reason ||
            'You have been blocked due to suspicious activity.',
          confirmButtonText: 'OK',
        }).then(() => {
          // Redirect after popup confirmation
          navigate('/userlogin');
        });
      }
    } catch (error) {
      console.error('Error sending incident:', error);
    }
  };

  return (
    <div className="page-wrapper">
      {/* Navbar */}
      <header className="navbar">
        <h1 className="logo">
          <span className="logo-cyan">NEURAL</span>{' '}
          <span className="logo-purple">GUARDIANS</span>
        </h1>
        <nav className="nav-buttons">
          <Link to="/userdashboard">
            <button className="btn btn-active">Portfolio</button>
          </Link>
          <Link to="/transaction">
            <button className="btn">Transactions</button>
          </Link>
        </nav>
      </header>

      {/* Grid Section */}
      <div className="bitcoin-grid">
        {/* Bitcoin Price with Chart */}
        <div className="card">
          <div className="card-header">
            <div>
              <h3 className="section-title">Bitcoin Price</h3>
              <p className="subtitle">24H Chart</p>
            </div>
            <div className="price-info">
              <p className="price-value">$42,850</p>
              <p className="price-change">+2.8%</p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={priceData}>
                <XAxis dataKey="time" stroke="#6b7280" />
                <YAxis
                  stroke="#6b7280"
                  domain={[0, 60000]}
                  tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    color: '#fff',
                  }}
                  formatter={(value) => [`$${value}`, 'Price']}
                />
                <Line
                  type="monotone"
                  dataKey="price"
                  stroke="#22d3ee"
                  strokeWidth={3}
                  dot={{ r: 4, fill: '#22d3ee' }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="card">
          <h3 className="section-title">Recent Transactions</h3>
          <ul className="transaction-list">
            {transactions.map((tx) => (
              <li
                key={tx.id}
                className="transaction-item"
                onClick={() => generateReport(tx)} // ✅ username included automatically
                style={{ cursor: 'pointer' }}
              >
                <div className="tx-left">
                  {tx.icon}
                  <div>
                    <p className="tx-type">{tx.type}</p>
                    <p className="tx-time">{tx.time}</p>
                  </div>
                </div>
                <div className="tx-right">
                  <p className="tx-amount">{tx.amount}</p>
                  <p className="tx-value">{tx.value}</p>
                  <p
                    className={`tx-status ${
                      tx.status === 'Completed'
                        ? 'status-completed'
                        : tx.status === 'Pending'
                        ? 'status-pending'
                        : 'status-failed'
                    }`}
                  >
                    {tx.status}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
