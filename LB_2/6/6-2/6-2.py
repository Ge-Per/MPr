from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


def save_to_db(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO texts (content) VALUES (?)", (data,))
    conn.commit()
    conn.close()


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/save_text", methods=["POST"])
def save_text():
    text = request.form.get("text")

    if text:
        save_to_db(text)
        return "Data saved successfully.", 200
    else:
        return "No text provided.", 400


if __name__ == "__main__":
    create_table()
    app.run(port=8000)
