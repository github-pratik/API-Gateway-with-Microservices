import React, { useState } from 'react';
import { login } from '../services/api';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log('Attempting login with:', username);
      const { token } = await login(username);
      console.log('Login successful, token:', token);
      onLogin(token);
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed');
    }
  };

  return (
    <div className="card p-4 mx-auto" style={{ maxWidth: '400px' }}>
      <h2 className="text-center mb-4">Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <input
            type="text"
            className="form-control"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          Login
        </button>
      </form>
    </div>
  );
}

export default Login; 