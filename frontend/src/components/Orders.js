import React, { useState, useEffect } from 'react';
import { getOrders, createOrder, getProducts } from '../services/api';

function Orders() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [newOrder, setNewOrder] = useState({
    product_id: '',
    quantity: 1
  });

  useEffect(() => {
    loadOrders();
    loadProducts();
  }, []);

  const loadOrders = async () => {
    try {
      const data = await getOrders();
      setOrders(data);
    } catch (error) {
      alert('Failed to load orders');
    }
  };

  const loadProducts = async () => {
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (error) {
      alert('Failed to load products');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const product = products.find(p => p.id === parseInt(newOrder.product_id));
      await createOrder({
        user_id: 1, // In real app, get from logged-in user
        items: [{
          product_id: parseInt(newOrder.product_id),
          quantity: parseInt(newOrder.quantity),
          price: product.price
        }]
      });
      loadOrders();
      setNewOrder({ product_id: '', quantity: 1 });
    } catch (error) {
      alert('Failed to create order');
    }
  };

  return (
    <div>
      <h2>Orders</h2>
      <div className="row">
        <div className="col-md-8">
          <table className="table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Total Amount</th>
                <th>Status</th>
                <th>Created At</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>${order.total_amount}</td>
                  <td>{order.status}</td>
                  <td>{new Date(order.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="col-md-4">
          <form onSubmit={handleSubmit}>
            <h4>Create New Order</h4>
            <div className="mb-3">
              <select
                className="form-control"
                value={newOrder.product_id}
                onChange={e => setNewOrder({...newOrder, product_id: e.target.value})}
              >
                <option value="">Select Product</option>
                {products.map(product => (
                  <option key={product.id} value={product.id}>
                    {product.name} - ${product.price}
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-3">
              <input
                type="number"
                className="form-control"
                placeholder="Quantity"
                min="1"
                value={newOrder.quantity}
                onChange={e => setNewOrder({...newOrder, quantity: e.target.value})}
              />
            </div>
            <button type="submit" className="btn btn-primary">Create Order</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Orders; 