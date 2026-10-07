import sqlite3
from datetime import datetime


DATABASE = "phishguard.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT NOT NULL,
            input_data TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            status TEXT NOT NULL,
            phishing_probability REAL,
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_scan(
    scan_type,
    input_data,
    risk_score,
    status,
    phishing_probability
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO scan_history (
            scan_type,
            input_data,
            risk_score,
            status,
            phishing_probability,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            scan_type,
            input_data,
            risk_score,
            status,
            phishing_probability,
            datetime.now().isoformat(
                timespec="seconds"
            ),
        ),
    )

    connection.commit()
    connection.close()


def get_scan_history():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM scan_history
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]