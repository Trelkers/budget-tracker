# Budget Tracker

A command line budget tracker written in Python, backed by SQLite. Add expenses under a category, list them back out sorted by date. Budget caps and a spend-vs-budget summary aren't wired up to the CLI yet, that part's still coming.

Built this to get comfortable with SQLite and actually finish something end to end instead of leaving it half done.

## Setup

Needs Python 3, nothing else.

Clone it and move in:

    git clone <repo-url>
    cd budget-tracker

Set up the database:

    python3 schema.py

That builds an empty `budget.db` with the `budgets` and `expenses` tables in it.

Categories now come with a monthly cap. To set or update one:

    python3 tracker.py budget --category groceries --cap 40000

Same cents convention as everywhere else so 40000 is a $400.00 cap. Run it again with a different '--cap' for the same category and it will update the existing cap rather than create a duplicate.

Money amounts are stored in cents everywhere, including `monthly_cap`. Kind of annoying to type but it avoids floating point rounding weirdness with dollars.

## Usage

Add an expense:

    python3 tracker.py add --amount 550 --category groceries --date 2026-08-18 --note "Coles"

`--amount` is cents, so 550 is $5.50. `--date` has to be `YYYY-MM-DD` or it gets rejected. `--note` is optional.

List everything:

    python3 tracker.py list

## Notes

`budgets` holds one row per category with a cap in cents. `expenses` points at a category through a foreign key, so the database itself stops you from logging an expense against a category that isn't there, no extra validation code needed for that part.

`sample_budget.db` comes with the repo already filled in with example data if you want to poke around without setting anything up. `budget.db` is your own local copy and it's gitignored, never gets committed.
