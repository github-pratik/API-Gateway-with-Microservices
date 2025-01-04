from functools import wraps
from flask import request
from prometheus_client import Counter, Histogram
import time

# Define metrics
REQUEST_COUNT = Counter(
    'gateway_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'gateway_request_latency_seconds',
    'Request latency',
    ['method', 'endpoint']
)

def track_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        start_time = time.time()
        
        response = f(*args, **kwargs)
        
        # Record metrics
        status_code = response[1] if isinstance(response, tuple) else 200
        endpoint = request.path
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(time.time() - start_time)
        
        return response
    
    return decorated 