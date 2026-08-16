import sqlite3
import os

def get_connection(db_name="budget.db", create_if_missing=False):
    # --- guard block ---
    # sqlite3.connect() does NOT error on a missing file — it silently creates an empty one
    # this check stops that: if the db doesn't exist and we're not explicitly allowed to make it, fail loudly
    if not create_if_missing and not os.path.exists(db_name):
        raise FileNotFoundError(f"'{db_name}' does not exist. Run schema.py first.")

    # --- connect block ---
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")  # sqlite ignores foreign key constraints unless you turn this on, every time
    return conn