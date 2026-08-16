import argparse
from db import get_connection
from datetime import datetime


def add_expense(amount, category, date, note=None):
    # --- validation block ---
    # reject bad data
    if amount <= 0:
        raise ValueError("Amount must be positive.")

    # catches things like "2026-13-45" or "tomorrow" before they corrupt the ORDER BY in list_expenses
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"'{date}' is not a valid date. Use YYYY-MM-DD.")

    conn = get_connection()
    cursor = conn.cursor()

    # --- category check block ---
    # pull every category that currently exists in the budgets table into a set
    valid_categories = {row[0] for row in cursor.execute("SELECT category FROM budgets")}
    if category not in valid_categories:
        conn.close()  # close before raising, don't leave the connection hanging open
        raise ValueError(f"'{category}' is not a known category. Valid: {', '.join(sorted(valid_categories))}")

    # --- insert block ---
    # ? placeholders instead of f-string interpolation — stops SQL injection and handles quoting for us
    cursor.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note),
    )
    conn.commit()   # nothing is actually saved to disk until commit() is called
    conn.close()


def list_expenses():
    # --- read block ---
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, amount, category, date, note FROM expenses ORDER BY date"
    ).fetchall()   # fetchall() pulls every row into a Python list, rather than streaming one at a time
    conn.close()
    return rows


def main():
    # --- CLI setup block ---
    # argparse turns "python tracker.py add --amount 25 ..." into actual Python values we can use
    parser = argparse.ArgumentParser(description="Budget tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)  # "command" will hold "add" or "list"

    # --- "add" subcommand definition ---
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=int, required=True, help="Amount in cents, e.g. 550 = $5.50")
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    add_parser.add_argument("--note", default=None)  # optional, defaults to nothing if not given

    # --- "list" subcommand definition ---
    # no extra arguments needed, just the command itself
    subparsers.add_parser("list", help="List all expenses")

    args = parser.parse_args()   # actually reads what the user typed in the terminal

    # --- dispatch block ---
    # decide which function to run based on which subcommand was typed
    if args.command == "add":
        try:
            add_expense(args.amount, args.category, args.date, args.note)
            print(f"Added: {args.category} ${args.amount / 100:.2f} on {args.date}")
        except ValueError as e:
            # catches the date, negative-amount, and unknown-category cases from add_expense()
            print(f"Error: {e}")
    elif args.command == "list":
        rows = list_expenses()
        if not rows:
            print("No expenses recorded.")
        for id_, amount, category, date, note in rows:
            note_str = f" — {note}" if note else ""   # only show the em-dash if there's actually a note
            print(f"[{id_}] {date}  {category:<15} ${amount / 100:.2f}{note_str}")  # :<15 left-pads category to line columns up


if __name__ == "__main__":
    main()   # only runs main() when this file is executed directly, not when imported