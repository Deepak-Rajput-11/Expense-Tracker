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

from reports import total_spending, category_wise_spending


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

        handle_view_expenses()

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
        for row in expense_table.get_children():
            expense_table.delete(row)

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
        for row in expense_table.get_children():
            expense_table.delete(row)

        messagebox.showinfo("No Results", "No expenses found for this date")
        return

    for row in expense_table.get_children():
        expense_table.delete(row)

    for expense in expenses:
        expense_table.insert("", tk.END, values=expense)


def handle_total_spending():
    total = total_spending()

    messagebox.showinfo("Total Spending", f"Total Spending: ₹{total:.2f}")


def handle_category_spending():
    category_totals = category_wise_spending()

    if category_totals.empty:
        messagebox.showinfo("No Data", "No expenses available for the report")
        return

    report = ""

    for category, amount in category_totals.items():
        report += f"{category}: ₹{amount:.2f}\n"

    messagebox.showinfo("Category-wise Spending", report)


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
root.geometry("700x700")

heading = tk.Label(root, text="Expense Tracker", font=("Arial", 20, "bold"))
heading.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(pady=5)

left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", padx=20)

right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", padx=20)


form_heading = tk.Label(
    left_frame,
    text="Expense Details",
    font=("Arial", 12, "bold"),
)
form_heading.pack(pady=(0, 10))

tools_heading = tk.Label(
    right_frame,
    text="Search & Reports",
    font=("Arial", 12, "bold"),
)
tools_heading.pack(pady=(0, 10))


date_label = tk.Label(left_frame, text="Date (YYYY-MM-DD):")
date_label.pack()

date_entry = tk.Entry(left_frame, width=30)
date_entry.pack(pady=5)

category_label = tk.Label(left_frame, text="Category:")
category_label.pack()

category_var = tk.StringVar()
category_var.set("Food")

category_dropdown = tk.OptionMenu(
    left_frame,
    category_var,
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other",
)
category_dropdown.pack(pady=5)

amount_label = tk.Label(left_frame, text="Amount:")
amount_label.pack()

amount_entry = tk.Entry(left_frame, width=30)
amount_entry.pack(pady=5)

description_label = tk.Label(left_frame, text="Description (Optional):")
description_label.pack()

description_entry = tk.Entry(left_frame, width=30)
description_entry.pack(pady=5)

add_button = tk.Button(left_frame, text="Add Expense", command=handle_add_expense)
add_button.pack(pady=15)


search_label = tk.Label(right_frame, text="Search Expense by ID:")
search_label.pack()

search_entry = tk.Entry(right_frame, width=15)
search_entry.pack(pady=5)

search_button = tk.Button(
    right_frame, text="Search Expense", command=handle_search_expense
)
search_button.pack(pady=5)
filter_category_label = tk.Label(right_frame, text="Filter by Category:")
filter_category_label.pack()

filter_category_var = tk.StringVar()
filter_category_var.set("Food")

filter_category_dropdown = tk.OptionMenu(
    right_frame,
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
    right_frame,
    text="Filter Category",
    command=handle_filter_category,
)
filter_category_button.pack(pady=5)


filter_date_label = tk.Label(right_frame, text="Filter by Date (YYYY-MM-DD):")
filter_date_label.pack()

filter_date_entry = tk.Entry(right_frame, width=15)
filter_date_entry.pack(pady=5)

filter_date_button = tk.Button(
    right_frame,
    text="Filter Date",
    command=handle_filter_date,
)
filter_date_button.pack(pady=5)


total_button = tk.Button(
    right_frame,
    text="Show Total Spending",
    command=handle_total_spending,
)
total_button.pack(pady=5)

category_spending_button = tk.Button(
    right_frame,
    text="Show Category Spending",
    command=handle_category_spending,
)
category_spending_button.pack(pady=5)

columns = ("ID", "Date", "Category", "Amount", "Description")

table_frame = tk.Frame(root)
table_frame.pack(pady=5)

view_button = tk.Button(
    table_frame,
    text="View Expenses",
    command=handle_view_expenses,
)
view_button.pack(pady=(0, 5))

tree_frame = tk.Frame(table_frame)
tree_frame.pack()

expense_table = ttk.Treeview(
    tree_frame,
    columns=columns,
    show="headings",
    height=6,
    selectmode="browse",
)

scrollbar = ttk.Scrollbar(
    tree_frame,
    orient="vertical",
    command=expense_table.yview,
)

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


action_frame = tk.Frame(root)
action_frame.pack(pady=5)

edit_button = tk.Button(
    action_frame,
    text="Edit Selected",
    command=handle_edit_expense,
)
edit_button.pack(side="left", padx=5)

update_button = tk.Button(
    action_frame,
    text="Update Expense",
    command=handle_update_expense,
)
update_button.pack(side="left", padx=5)

delete_button = tk.Button(
    action_frame,
    text="Delete Selected",
    command=handle_delete_expense,
)
delete_button.pack(side="left", padx=5)

handle_view_expenses()

root.mainloop()
