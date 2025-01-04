from flask import Flask, request, jsonify
from auth import require_auth, auth_bp
from rate_limiter import rate_limit
from telemetry import track_request
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["https://yourusername.github.io", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
app.register_blueprint(auth_bp)

# Service registry (in production, use service discovery)
SERVICES = {
    'users': os.getenv('USER_SERVICE_URL', 'http://user-service:5001'),
    'orders': os.getenv('ORDER_SERVICE_URL', 'http://order-service:5002'),
    'products': os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:5003')
}

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_auth
@rate_limit(max_requests=100, window_seconds=60)
@track_request
def gateway_route(service, path):
    if service not in SERVICES:
        return jsonify({'error': 'Service not found'}), 404
    
    service_url = f"{SERVICES[service]}/{path}"
    
    try:
        response = requests.request(
            method=request.method,
            url=service_url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            params=request.args
        )
        
        return (
            response.content,
            response.status_code,
            response.headers.items()
        )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Service unavailable', 'details': str(e)}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 