import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AuthPage.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const loginRes = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
      });

      const loginData = await loginRes.json();

      let status = 'failed';
      if (loginRes.ok && loginData.success) {
        status = 'success';
      }

      // Send incident
      const incidentPayload = {
        type: 'login',
        username: email,
        status: status,
      };

      await fetch('http://localhost:8000/incident', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(incidentPayload),
      });

      // Show backend message
      setMessage(loginData.message || 'Something went wrong');
      setIsError(status !== 'success');

      // 🔔 Also show an alert
      alert(loginData.message || 'Something went wrong');

      // Redirect if login successful
      if (status === 'success') {
        setTimeout(() => {
          navigate('/userdashboard', { state: { username: email } }); // ✅ pass username
        }, 1500);
      }
    } catch (err) {
      console.error('Login error:', err);
      setMessage('Something went wrong. Please try again later.');
      setIsError(true);
      alert('Something went wrong. Please try again later.');
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h1 className="brand">
          <span className="logo-cyan">NEURAL</span>{' '}
          <span className="logo-purple">GUARDIANS</span>
        </h1>

        <h2 className="form-title">User Login</h2>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className="btn-primary">
            Login
          </button>
        </form>

        {/* Message area */}
        {message && (
          <p
            style={{
              color: isError ? 'red' : 'green',
              marginTop: '10px',
              fontWeight: 'bold',
            }}
          >
            {message}
          </p>
        )}

        <p className="toggle-text">
          Don’t have an account?{' '}
          <Link to="/usersignup" className="toggle-btn">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}
