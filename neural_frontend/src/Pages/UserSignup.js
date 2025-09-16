import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './AuthPage.css';

export default function SignupPage() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message);
        // optionally redirect to login page
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error(error);
      alert('Registration failed');
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
            name="username"
            placeholder="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />

          <button type="submit" className="btn-primary">
            Sign Up
          </button>
        </form>

        <p className="toggle-text">
          Already have an account?{' '}
          <Link to="/userlogin" className="toggle-btn">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}
