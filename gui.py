import tkinter as tk
from tkinter import messagebox, ttk

from database import (
    add_expense,
    view_expenses,
    delete_expense,
    search_expense,
    update_expense,
    filter_by_category,
    filter_by_date,
)

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


editing_expense_id = None


def handle_filter_category():
    category = filter_category_var.get()

    expenses = filter_by_category(category)

    if not expenses:
        messagebox.showinfo("No Results", "No expenses found for this category")
        return

    for row in expense_table.get_children():
        expense_table.delete(row)

    for expense in expenses:
        expense_table.insert("", tk.END, values=expense)


def handle_filter_date():
    expense_date = filter_date_entry.get()

    if not validate_date(expense_date):
        messagebox.showerror("Error", "Please enter a valid date")
        return

    expenses = filter_by_date(expense_date)

    if not expenses:
        messagebox.showinfo("No Results", "No expenses found for this date")
        return

    for row in expense_table.get_children():
        expense_table.delete(row)

    for expense in expenses:
        expense_table.insert("", tk.END, values=expense)


def handle_edit_expense():
    global editing_expense_id

    selected_item = expense_table.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to edit")
        return

    expense_data = expense_table.item(selected_item[0], "values")

    editing_expense_id = expense_data[0]

    date_entry.delete(0, tk.END)
    date_entry.insert(0, expense_data[1])

    category_var.set(expense_data[2])

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, expense_data[3])

    description_entry.delete(0, tk.END)
    description_entry.insert(0, expense_data[4])


def handle_update_expense():
    global editing_expense_id

    if editing_expense_id is None:
        messagebox.showerror("Error", "Please select an expense to edit first")
        return

    expense_date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not (
        validate_date(expense_date)
        and validate_category(category)
        and validate_amount(amount)
    ):
        messagebox.showerror("Error", "Invalid expense data")
        return

    update_expense(
        editing_expense_id,
        expense_date,
        category,
        float(amount),
        description,
    )

    messagebox.showinfo("Success", "Expense updated successfully")
    handle_view_expenses()

    editing_expense_id = None

    date_entry.delete(0, tk.END)
    category_var.set("Food")
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.focus()


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
root.geometry("700x750")

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


filter_category_label = tk.Label(root, text="Filter by Category:")
filter_category_label.pack()

filter_category_var = tk.StringVar()
filter_category_var.set("Food")

filter_category_dropdown = tk.OptionMenu(
    root,
    filter_category_var,
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other",
)
filter_category_dropdown.pack(pady=5)

filter_category_button = tk.Button(
    root, text="Filter Category", command=handle_filter_category
)
filter_category_button.pack(pady=5)


filter_date_label = tk.Label(root, text="Filter by Date (YYYY-MM-DD):")
filter_date_label.pack()

filter_date_entry = tk.Entry(root, width=15)
filter_date_entry.pack(pady=5)

filter_date_button = tk.Button(root, text="Filter Date", command=handle_filter_date)
filter_date_button.pack(pady=5)


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


edit_button = tk.Button(root, text="Edit Selected", command=handle_edit_expense)
edit_button.pack(pady=5)

update_button = tk.Button(root, text="Update Expense", command=handle_update_expense)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Selected", command=handle_delete_expense)
delete_button.pack(pady=10)

root.mainloop()
