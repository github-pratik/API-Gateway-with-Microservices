import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">Microservices Demo</Link>
        <div className="navbar-nav">
          <Link className="nav-link" to="/products">Products</Link>
          <Link className="nav-link" to="/orders">Orders</Link>
          <Link className="nav-link" to="/users">Users</Link>
          <button className="btn btn-outline-light ms-2" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 