import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "data", "hri_system.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    """Establish and return a connection to the SQLite database with foreign keys enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    """Automatically create the SQLite database and tables on first run."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, "r") as schema_file:
            cursor.executescript(schema_file.read())
        conn.commit()
        print("Database initialized successfully.")
    else:
        print(f"Error: Schema file not found at {SCHEMA_PATH}")

    conn.close()


if __name__ == "__main__":
    initialize_database()