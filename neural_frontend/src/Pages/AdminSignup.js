import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AuthPage.css';

export default function SignupPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState(''); // used as username
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/adminregister', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email, // using email as username
          password: password,
          full_name: fullName, // optional field
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message || 'Account created successfully!');
        // Optionally redirect to login after registration
        setTimeout(() => navigate('/adminlogin'), 1500);
      } else {
        setError(data.error || 'Registration failed');
      }
    } catch (err) {
      console.error('Error registering admin:', err);
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

        <h2 className="form-title">Create Account</h2>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            placeholder="Full Name"
            required
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
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
          <input
            type="password"
            placeholder="Confirm Password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />

          <button type="submit" className="btn-primary">
            Sign Up
          </button>
        </form>

        {error && <p className="error-text">{error}</p>}
        {success && <p className="success-text">{success}</p>}

        <p className="toggle-text">
          Already have an account?{' '}
          <Link to="/adminlogin" className="toggle-btn">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
