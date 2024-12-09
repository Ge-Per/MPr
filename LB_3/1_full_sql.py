import sqlite3
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Path to the SQLite database for user management and product catalog
db_file = 'shop.db'


# Function to get a connection to the database
def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


# Function to initialize the database (create tables and insert default user if needed)
def init_db():
    conn = get_db_connection()
    # Create users table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
    # Create catalog table
    conn.execute('''CREATE TABLE IF NOT EXISTS catalog (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity INTEGER NOT NULL,
                        warehouse TEXT
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


# Verify password by checking the username and password in the users database
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
    conn = get_db_connection()

    if request.method == 'GET':
        # Get all items from the catalog
        items = conn.execute('SELECT * FROM catalog').fetchall()
        catalog = [dict(item) for item in items]  # Convert rows to dicts
        conn.close()
        return jsonify(format_response(catalog)), 200

    elif request.method == 'POST':
        # Create a new item
        new_item = request.get_json()
        if new_item and "name" in new_item and "price" in new_item and "quantity" in new_item:
            conn.execute('''INSERT INTO catalog (name, price, quantity, warehouse)
                            VALUES (?, ?, ?, ?)''',
                         (new_item["name"], new_item["price"], new_item["quantity"], new_item.get("warehouse", "")))
            conn.commit()
            conn.close()
            return jsonify({"message": "Item added", "item": new_item}), 201
        else:
            conn.close()
            return jsonify({"error": "Invalid item data"}), 400


# Endpoint to handle PUT and DELETE for specific item /items/<id>
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def handle_single_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM catalog WHERE id = ?', (item_id,)).fetchone()

    if request.method == 'GET':
        # Get a specific item by ID
        if item:
            return jsonify(format_response(dict(item))), 200
        conn.close()
        return jsonify(format_response(None, "Item not found")), 404

    elif request.method == 'PUT':
        # Update an existing item
        if not item:
            conn.close()
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

        conn.execute('''UPDATE catalog SET name = ?, price = ?, quantity = ?, warehouse = ? WHERE id = ?''',
                     (item["name"], item["price"], item["quantity"], item["warehouse"], item_id))
        conn.commit()
        conn.close()
        return jsonify(format_response(dict(item))), 200

    elif request.method == 'DELETE':
        # Delete an item
        if not item:
            conn.close()
            return jsonify(format_response(None, "Item not found")), 404

        conn.execute('DELETE FROM catalog WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        return jsonify(format_response(None, "Item deleted")), 200


if __name__ == '__main__':
    # Initialize the database (create tables and add default users)
    init_db()

    # Start the Flask application
    app.run(host='0.0.0.0', port=8000)
