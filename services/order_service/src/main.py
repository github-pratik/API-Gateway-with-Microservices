from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage
orders = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.get_json()
    order['id'] = len(orders) + 1
    order['created_at'] = datetime.utcnow().isoformat()
    orders.append(order)
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 