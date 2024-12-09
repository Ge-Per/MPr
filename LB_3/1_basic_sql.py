import sqlite3
from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Product catalog
catalog = {
    1: {"name": "Apple", "price": 15, "quantity": 50, "warehouse": "A1"},
    2: {"name": "Banana", "price": 35, "quantity": 100, "warehouse": "B2"},
    3: {"name": "Cherry", "price": 25, "quantity": 20, "warehouse": "C3"},
}

# Path to the SQLite database
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
    users = load_users()  # Load users from the file each time
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

# Endpoint to get all items
@app.route('/items', methods=['GET'])
@auth.login_required
def get_all_items():
    return jsonify(format_response(catalog)), 200


# Endpoint to get a specific item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item_by_id(item_id):
    item = catalog.get(item_id)
    if item:
        return jsonify(format_response(item)), 200
    return jsonify(format_response(None, "Item not found")), 404

if __name__ == '__main__':
    init_db()

    app.run(host='0.0.0.0', port=8000)
