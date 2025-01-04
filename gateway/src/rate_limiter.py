from functools import wraps
from flask import request, jsonify
import redis
import time
import os

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
print(f"Connecting to Redis at: {redis_url}")

try:
    redis_client = redis.from_url(redis_url)
    # Test Redis connection
    redis_client.ping()
    print("Redis connection successful!")
except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")

def rate_limit(max_requests=100, window_seconds=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            # Create a key for this IP
            key = f"rate_limit:{client_ip}"
            
            # Get current count for this IP
            count = redis_client.get(key)
            if count is None:
                # First request, set count to 1 with expiry
                redis_client.setex(key, window_seconds, 1)
            else:
                count = int(count)
                if count >= max_requests:
                    return jsonify({'error': 'Rate limit exceeded'}), 429
                redis_client.incr(key)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator 