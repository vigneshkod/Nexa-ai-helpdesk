
import sqlite3
from pathlib import Path

# Store the database in the main project folder
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "helpdesk.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            channel TEXT DEFAULT 'Text Chat',
            status TEXT DEFAULT 'Open',
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_all_tickets():

    connection = get_connection()

    tickets = connection.execute("""
        SELECT * FROM tickets
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return tickets


def get_ticket(ticket_id):

    connection = get_connection()

    ticket = connection.execute("""
        SELECT * FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,)).fetchone()

    connection.close()

    return ticket
