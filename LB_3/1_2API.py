from flask import Flask, jsonify

app = Flask(__name__)

# Product catalog
catalog = {
    1: {"name": "Apple", "price": 15, "quantity": 50, "warehouse": "A1"},
    2: {"name": "Banana", "price": 35, "quantity": 100, "warehouse": "B2"},
    3: {"name": "Cherry", "price": 25, "quantity": 20, "warehouse": "C3"},
}

# Unified response format
def format_response(data, message="Success"):
    return {
        "status": "ok",
        "message": message,
        "data": data,
    }

# Endpoint to get all items
@app.route('/items', methods=['GET'])
def get_all_items():
    return jsonify(format_response(catalog)), 200

# Endpoint to get a specific item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    item = catalog.get(item_id)
    if item:
        return jsonify(format_response(item)), 200
    return jsonify(format_response(None, "Item not found")), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
