import React, { useState } from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Products from './components/Products';
import Orders from './components/Orders';
import Users from './components/Users';
import Navbar from './components/Navbar';
import Register from './components/Register';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const toggleRegister = () => {
    setShowRegister(!showRegister);
  };

  return (
    <Router>
      {token && <Navbar />}
      <div className="container mt-4">
        <Routes>
          <Route 
            path="/login" 
            element={
              !token ? (
                showRegister ? (
                  <Register onToggle={toggleRegister} />
                ) : (
                  <Login onLogin={handleLogin} onToggle={toggleRegister} />
                )
              ) : (
                <Navigate to="/products" />
              )
            } 
          />
          <Route path="/products" element={token ? <Products /> : <Navigate to="/login" />} />
          <Route path="/orders" element={token ? <Orders /> : <Navigate to="/login" />} />
          <Route path="/users" element={token ? <Users /> : <Navigate to="/login" />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 