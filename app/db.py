import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "appointments.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    datetime TEXT NOT NULL,
    message TEXT
)
"""

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()

def create_appointment(name: str, email: str, datetime: str, message: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO appointments (name, email, datetime, message) VALUES (?, ?, ?, ?)",
            (name, email, datetime, message),
        )
        conn.commit()

def fetch_appointments():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, name, email, datetime, message FROM appointments ORDER BY datetime DESC"
        ).fetchall()
        return [dict(row) for row in rows]
