import tkinter as tk
from tkinter import messagebox, ttk

from database import add_expense, view_expenses, delete_expense, search_expense
from validation import validate_date, validate_category, validate_amount


def handle_add_expense():
    expense_date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if (
        validate_date(expense_date)
        and validate_category(category)
        and validate_amount(amount)
    ):
        add_expense(expense_date, category, float(amount), description)
        messagebox.showinfo("Success", "Expense added successfully")

        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        category_var.set("Food")
        date_entry.focus()

    else:
        messagebox.showerror("Error", "Invalid expense data")


def handle_view_expenses():
    expenses = view_expenses()

    for row in expense_table.get_children():
        expense_table.delete(row)

    for expense in expenses:
        expense_table.insert("", tk.END, values=expense)


def handle_search_expense():
    expense_id = search_entry.get()

    if expense_id == "":
        messagebox.showerror("Error", "Please enter an Expense ID")
        return

    expense = search_expense(expense_id)

    if expense is None:
        messagebox.showerror("Error", "Expense not found")
        return

    for row in expense_table.get_children():
        expense_table.delete(row)

    expense_table.insert("", tk.END, values=expense)


def handle_delete_expense():
    selected_item = expense_table.selection()

    if selected_item:
        expense_data = expense_table.item(selected_item[0], "values")
        expense_id = expense_data[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Expense ID {expense_id}?",
        )

        if confirm:
            delete_expense(expense_id)
            messagebox.showinfo("Success", "Expense deleted successfully")
            handle_view_expenses()

    else:
        messagebox.showerror("Error", "Please select an expense to delete")


root = tk.Tk()

root.title("Expense Tracker")
root.geometry("700x650")

heading = tk.Label(root, text="Expense Tracker", font=("Arial", 20, "bold"))
heading.pack(pady=20)

date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.pack()

date_entry = tk.Entry(root, width=30)
date_entry.pack(pady=5)

category_label = tk.Label(root, text="Category:")
category_label.pack()

category_var = tk.StringVar()
category_var.set("Food")

category_dropdown = tk.OptionMenu(
    root, category_var, "Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"
)

category_dropdown.pack(pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.pack()

amount_entry = tk.Entry(root, width=30)
amount_entry.pack(pady=5)

description_label = tk.Label(root, text="Description (Optional):")
description_label.pack()

description_entry = tk.Entry(root, width=30)
description_entry.pack(pady=5)


add_button = tk.Button(root, text="Add Expense", command=handle_add_expense)
add_button.pack(pady=15)

view_button = tk.Button(root, text="View Expenses", command=handle_view_expenses)
view_button.pack(pady=5)

search_label = tk.Label(root, text="Search Expense by ID:")
search_label.pack()

search_entry = tk.Entry(root, width=15)
search_entry.pack(pady=5)

search_button = tk.Button(root, text="Search Expense", command=handle_search_expense)
search_button.pack(pady=5)

columns = ("ID", "Date", "Category", "Amount", "Description")

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

expense_table = ttk.Treeview(
    table_frame, columns=columns, show="headings", height=8, selectmode="browse"
)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=expense_table.yview)

expense_table.configure(yscrollcommand=scrollbar.set)

for column in columns:
    expense_table.heading(column, text=column)

expense_table.column("ID", width=50)
expense_table.column("Date", width=100)
expense_table.column("Category", width=100)
expense_table.column("Amount", width=80)
expense_table.column("Description", width=180)

expense_table.pack(side="left")
scrollbar.pack(side="right", fill="y")


delete_button = tk.Button(root, text="Delete Selected", command=handle_delete_expense)
delete_button.pack(pady=10)

root.mainloop()
