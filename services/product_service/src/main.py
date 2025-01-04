from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Add this constant at the top
DB_PATH = 'data/products.db'

with app.app_context():
    def init_db():
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                stock INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    init_db()

@app.route('/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DB_PATH)  # Updated
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = [{'id': row[0], 'name': row[1], 'description': row[2],
                'price': row[3], 'stock': row[4], 'created_at': row[5]} 
               for row in c.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = sqlite3.connect(DB_PATH)  # Updated
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    conn.close()
    
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
        
    return jsonify({
        'id': product[0],
        'name': product[1],
        'description': product[2],
        'price': product[3],
        'stock': product[4],
        'created_at': product[5]
    })

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data or 'stock' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        conn = sqlite3.connect(DB_PATH)  # Updated
        c = conn.cursor()
        c.execute(
            '''INSERT INTO products (name, description, price, stock) 
               VALUES (?, ?, ?, ?)''',
            (data['name'], data.get('description', ''), data['price'], data['stock'])
        )
        conn.commit()
        product_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'id': product_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'price': data['price'],
            'stock': data['stock']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    try:
        conn = sqlite3.connect(DB_PATH)  # Updated
        c = conn.cursor()
        
        # Check if product exists
        c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        if not c.fetchone():
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
            
        # Update fields that are provided
        updates = []
        values = []
        for field in ['name', 'description', 'price', 'stock']:
            if field in data:
                updates.append(f'{field} = ?')
                values.append(data[field])
        
        if updates:
            values.append(product_id)
            c.execute(
                f'UPDATE products SET {", ".join(updates)} WHERE id = ?',
                values
            )
            conn.commit()
            
        conn.close()
        return jsonify({'message': 'Product updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003) 