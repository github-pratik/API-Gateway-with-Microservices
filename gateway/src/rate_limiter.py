from functools import wraps
from flask import request, jsonify
import redis
import time
import os

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url)

def rate_limit(max_requests: int, window_seconds: int):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            # Create a unique key for this IP
            key = f"rate_limit:{client_ip}"
            
            # Get current request count
            current = redis_client.get(key)
            
            if current is None:
                # First request, set counter
                redis_client.setex(key, window_seconds, 1)
            elif int(current) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            else:
                # Increment counter
                redis_client.incr(key)
            
            return f(*args, **kwargs)
        return decorated
    return decorator 