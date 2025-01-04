from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": "*",
        "allow_headers": "*"
    }
})

# In-memory storage
users = []

@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print("Received registration data:", {
            **data,
            'password': '***hidden***'  # Don't log actual password
        })
        
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
        print("User registered successfully:", {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        })
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print("Registration error:", str(e))
        return jsonify({'error': str(e)}), 500 