from schema import SCHEMA_SQL
from db import get_connection

conn = get_connection("sample_budget.db")
cursor = conn.cursor()
cursor.executescript(SCHEMA_SQL)

budgets = [
    ("groceries", 40000),
    ("transport", 15000),
    ("entertainment", 10000),
    ("rent", 250000),
    ("clothes", 8000),
]

expenses = [
    (5200, "groceries", "2026-08-02", "Woolworths"),
    (4300, "groceries", "2026-08-09", "Coles"),
    (3800, "groceries", "2026-08-15", "Coles"),
    (1200, "transport", "2026-08-03", "Myki"),
    (2500, "entertainment", "2026-08-05", "Cinema"),
    (4500, "entertainment", "2026-08-14", "Concert ticket"),
    (250000, "rent", "2026-08-01", None),
    (9500, "clothes", "2026-08-10", "Armani Jeans"),
]

cursor.executemany(
    "INSERT INTO budgets (category, monthly_cap) VALUES (?, ?)", budgets
)
cursor.executemany(
    "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
    expenses,
)

conn.commit()
conn.close()