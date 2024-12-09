import sqlite3
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Product catalog
catalog = {
    1: {"name": "Apple", "price": 15, "quantity": 50, "warehouse": "A1"},
    2: {"name": "Banana", "price": 35, "quantity": 100, "warehouse": "B2"},
    3: {"name": "Cherry", "price": 25, "quantity": 20, "warehouse": "C3"},
}

# Path to the SQLite database for user management
db_file = 'users.db'


# Function to get a connection to the database
def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


# Function to initialize the database (create tables and insert default user if needed)
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
    # Insert a default user if the table is empty
    conn.execute('''INSERT OR IGNORE INTO users (username, password)
                    VALUES ('admin', 'password')''')
    conn.commit()
    conn.close()


# Function to load users from the database
def load_users():
    conn = get_db_connection()
    users = {}
    rows = conn.execute('SELECT username, password FROM users').fetchall()
    for row in rows:
        users[row['username']] = row['password']
    conn.close()
    return users


# Verify password by checking the username and password in the users dictionary
@auth.verify_password
def verify_password(username, password):
    users = load_users()  # Load users from the database each time
    if username in users and users[username] == password:
        return username
    return None


# Unified response format
def format_response(data, message="Success"):
    return {
        "status": "ok",
        "message": message,
        "data": data,
    }


# Endpoint to handle all methods (GET, POST) for /items
@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def handle_items():
    if request.method == 'GET':
        # Return all items
        return jsonify(format_response(catalog)), 200

    elif request.method == 'POST':
        # Create a new item
        new_item = request.get_json()
        if new_item and "name" in new_item and "price" in new_item and "quantity" in new_item:
            new_id = max(catalog.keys()) + 1 if catalog else 1
            catalog[new_id] = new_item
            return jsonify({"message": "Item added", "item": new_item}), 201
        else:
            return jsonify({"error": "Invalid item data"}), 400


# Endpoint to handle PUT and DELETE for specific item /items/<id>
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def handle_single_item(item_id):
    item = catalog.get(item_id)

    if request.method == 'GET':
        # Get a specific item by ID
        if item:
            return jsonify(format_response(item)), 200
        return jsonify(format_response(None, "Item not found")), 404

    elif request.method == 'PUT':
        # Update an existing item
        if not item:
            return jsonify(format_response(None, "Item not found")), 404

        data = request.get_json()
        if "name" in data:
            item["name"] = data["name"]
        if "price" in data:
            item["price"] = data["price"]
        if "quantity" in data:
            item["quantity"] = data["quantity"]
        if "warehouse" in data:
            item["warehouse"] = data["warehouse"]

        return jsonify(format_response(item)), 200

    elif request.method == 'DELETE':
        # Delete an item
        if not item:
            return jsonify(format_response(None, "Item not found")), 404

        del catalog[item_id]
        return jsonify(format_response(None, "Item deleted")), 200


if __name__ == '__main__':
    # Initialize the database (create tables and add default users)
    init_db()

    # Start the Flask application
    app.run(host='0.0.0.0', port=8000)
