# --- schema definition block ---
# raw SQL, kept as a string so both this file and seed.py can import and reuse it
SCHEMA_SQL = """
CREATE TABLE budgets (
    category TEXT PRIMARY KEY,
    monthly_cap INTEGER NOT NULL
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    amount INTEGER NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (category) REFERENCES budgets(category)
);
"""

from db import get_connection

# --- execution guard ---
# without this, seed.py importing SCHEMA_SQL from this file would ALSO run the block below
# and silently create/touch budget.db as a side effect of just importing a variable
if __name__ == "__main__":
    conn = get_connection(create_if_missing=True)  # the one place in the project allowed to create the db file
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)   # executescript runs multiple ; separated statements at once
    conn.commit()
    conn.close()