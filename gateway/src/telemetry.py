import time
from functools import wraps
import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

def track_request(service_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            # Track request count
            redis_client.incr(f"{service_name}_requests")
            
            try:
                response = f(*args, **kwargs)
                # Track successful requests
                redis_client.incr(f"{service_name}_success")
                return response
            except Exception as e:
                # Track failed requests
                redis_client.incr(f"{service_name}_errors")
                raise e
            finally:
                # Track response time
                execution_time = time.time() - start_time
                redis_client.lpush(f"{service_name}_response_times", execution_time)
                
        return decorated_function
    return decorator

def get_service_metrics(service_name):
    return {
        'total_requests': int(redis_client.get(f"{service_name}_requests") or 0),
        'successful_requests': int(redis_client.get(f"{service_name}_success") or 0),
        'errors': int(redis_client.get(f"{service_name}_errors") or 0),
        'avg_response_time': float(redis_client.lrange(f"{service_name}_response_times", 0, -1)[0]) if redis_client.llen(f"{service_name}_response_times") > 0 else 0
    } 