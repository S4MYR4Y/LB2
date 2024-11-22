from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    """
    Initializes the database by creating the 'data' table if it doesn't exist.
    """
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        conn.commit()

def get_db_connection():
    try:
        conn = sqlite3.connect('data.db')
        conn.row_factory = sqlite3.Row  # Convert rows to dictionaries for easier access
        return conn
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

@app.route('/', methods=['POST'])
def add_data():
    text = request.get_data(as_text=True)
    if not text:
        return jsonify({"error": "No text provided"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection error"}), 500  # Internal server error

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (content) VALUES (?)", (text,))
        conn.commit()
        return jsonify(f'Message: "{text}" has been successfully posted!'), 201  # Created

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return jsonify({"error": "Error adding data"}), 500  # Internal server error

    finally:
        if conn:
            conn.close()  # Ensure connection is closed properly

if __name__ == "__main__":
    init_db()  # Call init_db to create the table if it doesn't exist
    app.run(port=8000, debug=True)