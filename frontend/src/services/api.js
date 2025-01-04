const API_URL = process.env.REACT_APP_API_URL;

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

export const login = async (username, password) => {
  try {
    const response = await fetch(`${API_URL}/auth/token`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      mode: 'no-cors',
      body: JSON.stringify({ username, password })
    });
    
    if (response.type === 'opaque') {
      // Handle opaque response
      return { token: 'dummy-token' }; // You'll need to handle this properly
    }
    
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const register = async (username, password, email) => {
  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password, email })
    });
    
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }
    
    console.log('Registration successful:', data);
    return data;
  } catch (error) {
    console.error('Registration error:', error);
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