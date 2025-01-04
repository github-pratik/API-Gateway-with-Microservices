from functools import wraps
from flask import Blueprint, request, jsonify
from jose import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '1f7caaa25723f45595796ce84a234b2a9771c4369913b9b468149c387f1a36ed')

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

@auth_bp.route('/auth/token', methods=['POST'])
def get_token():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'error': 'Username required'}), 400
        
    token = jwt.encode(
        {
            'sub': data['username'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    print(f"Generated token: {token}")
    return jsonify({'token': token}) 