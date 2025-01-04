const API_URL = 'https://apigatewaywithmicroservice-7rosn6upq-github-pratiks-projects.vercel.app';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

export const login = async (username) => {
  try {
    const response = await fetch(`${API_URL}/auth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username })
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
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