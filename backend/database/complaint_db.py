import sqlite3
from pathlib import Path

DB_PATH = "complaints.db"

def init_db():
    """Create the simplified complaints table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                query TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("✅ complaints.db initialized with email, query, and summary only.")

def insert_complaint(email, query, summary):
    """Insert a simplified complaint into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO complaints (email, query, summary)
            VALUES (?, ?, ?)
        """, (email, query, summary))
        conn.commit()
    print(f"✅ Complaint inserted for: {email}")
