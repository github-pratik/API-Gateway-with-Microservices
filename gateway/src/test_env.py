import os
import redis
import requests

def test_environment():
    # Test environment variables
    required_vars = [
        'JWT_SECRET_KEY',
        'USER_SERVICE_URL',
        'ORDER_SERVICE_URL',
        'PRODUCT_SERVICE_URL',
        'REDIS_URL'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        print(f"{var}: {'✓' if value else '✗'} ({value if var != 'JWT_SECRET_KEY' else '***'})")

    # Test Redis connection
    try:
        redis_client = redis.from_url(os.getenv('REDIS_URL'))
        redis_client.ping()
        print("Redis connection: ✓")
    except Exception as e:
        print(f"Redis connection: ✗ ({str(e)})")

    # Test service connections
    services = ['user', 'order', 'product']
    for service in services:
        url = os.getenv(f'{service.upper()}_SERVICE_URL')
        try:
            response = requests.get(f"{url}/health")
            print(f"{service} service: {'✓' if response.status_code == 200 else '✗'}")
        except Exception as e:
            print(f"{service} service: ✗ ({str(e)})")

if __name__ == "__main__":
    test_environment() 