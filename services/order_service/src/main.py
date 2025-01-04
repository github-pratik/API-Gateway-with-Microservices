from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import requests
import os

app = Flask(__name__)

# Add this constant at the top
DB_PATH = 'data/orders.db'

with app.app_context():
    def init_db():
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        conn.commit()
        conn.close()
    
    init_db()

@app.route('/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get('user_id')
    conn = sqlite3.connect(DB_PATH)  # Updated
    c = conn.cursor()
    
    if user_id:
        c.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,))
    else:
        c.execute('SELECT * FROM orders')
        
    orders = [{'id': row[0], 'user_id': row[1], 'total_amount': row[2], 
               'status': row[3], 'created_at': row[4]} for row in c.fetchall()]
    conn.close()
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'items' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        conn = sqlite3.connect(DB_PATH)  # Updated
        c = conn.cursor()
        
        # Calculate total amount
        total_amount = sum(item['price'] * item['quantity'] for item in data['items'])
        
        # Create order
        c.execute(
            'INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)',
            (data['user_id'], total_amount, 'pending')
        )
        order_id = c.lastrowid
        
        # Create order items
        for item in data['items']:
            c.execute(
                '''INSERT INTO order_items 
                   (order_id, product_id, quantity, price) 
                   VALUES (?, ?, ?, ?)''',
                (order_id, item['product_id'], item['quantity'], item['price'])
            )
            
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': order_id,
            'user_id': data['user_id'],
            'total_amount': total_amount,
            'status': 'pending',
            'items': data['items']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 