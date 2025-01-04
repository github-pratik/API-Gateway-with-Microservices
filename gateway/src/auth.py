from functools import wraps
from flask import request, jsonify
import jwt
import os

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

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
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated 