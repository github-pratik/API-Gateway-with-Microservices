from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
import bcrypt  # Add password hashing

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["https://github-pratik.github.io"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Add before all routes
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# In-memory storage with password hashing
users = []
products = []
orders = []

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            request.user = payload
        except (jwt.JWTError, IndexError):
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    
    return decorated

# Auth routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
        
    # Check if user exists
    if any(u['username'] == data['username'] for u in users):
        return jsonify({'error': 'Username already exists'}), 409
        
    # Hash password
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    user = {
        'id': len(users) + 1,
        'username': data['username'],
        'password': hashed,
        'email': data.get('email', '')
    }
    users.append(user)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/auth/token', methods=['POST'])
def get_token():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
        
    user = next((u for u in users if u['username'] == data['username']), None)
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
        
    token = jwt.encode(
        {
            'sub': user['username'],
            'id': user['id'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        JWT_SECRET_KEY,
        algorithm='HS256'
    )
    return jsonify({'token': token, 'user_id': user['id']})

# User routes
@app.route('/users/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        data = request.get_json()
        user = {
            'id': len(users) + 1,
            'username': data['username'],
            'email': data['email']
        }
        users.append(user)
        return jsonify(user), 201
    return jsonify(users)

# Product routes
@app.route('/products/products', methods=['GET', 'POST'])
@require_auth
def handle_products():
    if request.method == 'POST':
        data = request.get_json()
        product = {
            'id': len(products) + 1,
            'name': data['name'],
            'price': data['price'],
            'stock': data['stock']
        }
        products.append(product)
        return jsonify(product), 201
    return jsonify(products)

# Order routes
@app.route('/orders/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'POST':
        data = request.get_json()
        order = {
            'id': len(orders) + 1,
            'user_id': data['user_id'],
            'items': data['items'],
            'total_amount': sum(item['price'] * item['quantity'] for item in data['items']),
            'status': 'pending'
        }
        orders.append(order)
        return jsonify(order), 201
    return jsonify(orders)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000))) 