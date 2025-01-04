from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Add this constant at the top
DB_PATH = 'data/users.db'

with app.app_context():
    def init_db():
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    init_db()

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DB_PATH)  # Updated
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = [{'id': row[0], 'username': row[1], 'email': row[2], 'created_at': row[3]} 
             for row in c.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)  # Updated
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'created_at': user[3]
    })

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        conn = sqlite3.connect(DB_PATH)  # Updated
        c = conn.cursor()
        c.execute(
            'INSERT INTO users (username, email) VALUES (?, ?)',
            (data['username'], data['email'])
        )
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'id': user_id,
            'username': data['username'],
            'email': data['email']
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 