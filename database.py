import sqlite3

conn = sqlite3.connect("expenses.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT
)
""")


def add_expense(date, category, amount, description):
    cursor.execute(
        "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
        (date, category, amount, description),
    )
    conn.commit()


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    return expenses


def search_expense(expense_id):
    cursor.execute("SELECT * FROM expenses WHERE expense_id = ?", (expense_id,))
    expense = cursor.fetchone()
    return expense


def update_expense(expense_id, date, category, amount, description):
    cursor.execute(
        """
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, description = ?
        WHERE expense_id = ?
        """,
        (date, category, amount, description, expense_id),
    )
    conn.commit()


def delete_expense(expense_id):
    cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
    conn.commit()
