from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Load customers data
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_customers():
    """Load customers from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "flask-mock-server"}), 200

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get paginated list of customers"""
    customers = load_customers()
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Validate parameters
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    
    # Calculate pagination
    total = len(customers)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    # Get paginated data
    paginated_customers = customers[start_idx:end_idx]
    
    return jsonify({
        "data": paginated_customers,
        "total": total,
        "page": page,
        "limit": limit
    }), 200

@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get single customer by ID"""
    customers = load_customers()
    
    # Find customer by ID
    customer = next((c for c in customers if c['customer_id'] == customer_id), None)
    
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    
    return jsonify({"data": customer}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)