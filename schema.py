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

import sqlite3

conn = sqlite3.connect("budget.db")
cursor = conn.cursor()
cursor.executescript(SCHEMA_SQL)
conn.commit()
conn.close()
