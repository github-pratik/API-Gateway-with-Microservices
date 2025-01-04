from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
products = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    product = request.get_json()
    product['id'] = len(products) + 1
    products.append(product)
    return jsonify(product), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003) 