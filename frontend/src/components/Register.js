import React, { useState } from 'react';
import { register } from '../services/api';

function Register({ onToggle }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await register(username, password);
      if (response.message) {
        alert('Registration successful! Please login.');
        onToggle();
      } else {
        setError(response.error || 'Registration failed');
      }
    } catch (error) {
      setError('Registration failed');
      console.error('Registration error:', error);
    }
  };

  return (
    <div className="card p-4 mx-auto" style={{ maxWidth: '400px' }}>
      <h2 className="text-center mb-4">Register</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <input
            type="text"
            className="form-control"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="password"
            className="form-control"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100 mb-3">
          Register
        </button>
        <button type="button" className="btn btn-link w-100" onClick={onToggle}>
          Already have an account? Login
        </button>
      </form>
    </div>
  );
}

export default Register; 