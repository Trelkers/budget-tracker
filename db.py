import sqlite3
import os

def get_connection(db_name="budget.db", create_if_missing=False):
    if not create_if_missing and not os.path.exists(db_name):
        raise FileNotFoundError(f"'{db_name}' does not exist. Run schema.py first.")
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

