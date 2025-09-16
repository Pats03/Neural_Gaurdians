import React from 'react';
import { Link, useLocation } from 'react-router-dom'; // ✅ Added useLocation
import './PortfolioDashboard.css';

export default function PortfolioDashboard() {
  const location = useLocation();
  const username = location.state?.username || 'guest'; // ✅ get username from login

  return (
    <div className="dashboard">
      {/* Navbar */}
      <header className="navbar">
        <h1 className="logo">
          <span className="logo-cyan">NEURAL</span>{' '}
          <span className="logo-purple">GUARDIANS</span>
        </h1>
        <nav className="nav-buttons">
          <Link to="/userdashboard" state={{ username }}>
            {' '}
            {/* ✅ Pass username forward */}
            <button className="btn btn-active">Portfolio</button>
          </Link>
          <Link to="/transaction" state={{ username }}>
            {' '}
            {/* ✅ Pass username to Transactions */}
            <button className="btn">Transactions</button>
          </Link>
        </nav>
      </header>

      {/* Dashboard Title */}
      <div className="title-section">
        <h2 className="title">Welcome, {username} 👋</h2>
        <p className="subtitle">Secure Digital Asset Management</p>
      </div>

      <div className="grid-3">
        {/* Portfolio Value Card */}
        <div className="card card-span-2">
          <h3 className="card-subtitle">Total Portfolio Value</h3>
          <p className="card-value">$127,845.67</p>
          <p className="card-change">+3,247.89 (+2.61%) 24h</p>

          <div className="card-details">
            <p>
              <span className="text-gray">Available:</span>{' '}
              <span className="text-cyan">$98,247.32</span>
            </p>
            <p>
              <span className="text-gray">Locked:</span>{' '}
              <span className="text-purple">$29,598.35</span>
            </p>
            <p>
              <span className="text-gray">Margin:</span>{' '}
              <span className="text-orange">$0.00</span>
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3 className="card-subtitle">Quick Actions</h3>
          <div className="actions">
            <button className="action-btn buy">+ Buy</button>
            <button className="action-btn sell">– Sell</button>
            <button className="action-btn transfer">↔ Transfer</button>
            <button className="action-btn flash">⚡ Flash Loan</button>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid-2">
        {/* Bitcoin Price */}
        <div className="card">
          <h3 className="card-subtitle">Bitcoin Price</h3>
          <p className="btc-price">$42,850</p>
          <p className="btc-change">+2.8%</p>
        </div>

        {/* Recent Transactions */}
        <div className="card">
          <h3 className="card-subtitle">Recent Transactions</h3>
          <ul className="transactions">
            <li>
              <span>Buy BTC</span>
              <span className="positive">+$500</span>
            </li>
            <li>
              <span>Sell ETH</span>
              <span className="negative">- $300</span>
            </li>
            <li>
              <span>Transfer USDT</span>
              <span className="neutral">$1,000</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
