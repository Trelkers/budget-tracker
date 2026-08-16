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

if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()