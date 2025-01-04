const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

export const login = async (username) => {
  const response = await fetch(`${API_URL}/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username })
  });
  return response.json();
};

export const getProducts = async () => {
  const response = await fetch(`${API_URL}/products/products`, {
    headers: getHeaders()
  });
  return response.json();
};

export const createProduct = async (product) => {
  const response = await fetch(`${API_URL}/products/products`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(product)
  });
  return response.json();
};

export const getOrders = async () => {
  const response = await fetch(`${API_URL}/orders/orders`, {
    headers: getHeaders()
  });
  return response.json();
};

export const createOrder = async (order) => {
  const response = await fetch(`${API_URL}/orders/orders`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(order)
  });
  return response.json();
};

export const getUsers = async () => {
  const response = await fetch(`${API_URL}/users/users`, {
    headers: getHeaders()
  });
  return response.json();
}; 