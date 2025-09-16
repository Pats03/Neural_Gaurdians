import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AuthPage.css';

export default function LoginPage() {
  const [email, setEmail] = useState(''); // store email input
  const [password, setPassword] = useState(''); // store password input
  const [error, setError] = useState(''); // store error messages
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/adminlogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email, // assuming email is used as username
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Login success:', data);
        // Redirect to admin dashboard (example)
        navigate('/admindashboard');
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      console.error('Error logging in:', err);
      setError('Server error. Try again later.');
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h1 className="brand">
          <span className="logo-cyan">NEURAL</span>{' '}
          <span className="logo-purple">GUARDIANS</span>
        </h1>

        <h2 className="form-title">Admin Login</h2>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit" className="btn-primary">
            Login
          </button>
        </form>

        {error && <p className="error-text">{error}</p>}

        <p className="toggle-text">
          Don’t have an account?{' '}
          <Link to="/adminsignup" className="toggle-btn">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}
