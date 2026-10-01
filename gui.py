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

from reports import (
    total_spending,
    category_wise_spending,
    expense_count,
    average_expense,
    highest_spending_category,
)


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
        refresh_total_spending()

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

    if category == "All Categories":
        handle_view_expenses()
        return

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


def refresh_total_spending():
    total = total_spending()
    total_spending_var.set(f"Overall Spending: ₹{total:.2f}")
    return total


def handle_total_spending():
    total = refresh_total_spending()
    count = expense_count()
    average = average_expense()
    highest_category = highest_spending_category()

    messagebox.showinfo(
        "Spending Summary",
        f"Total Spending: ₹{total:.2f}\n"
        f"Number of Expenses: {count}\n"
        f"Average Expense: ₹{average:.2f}\n"
        f"Highest Spending Category: {highest_category}",
    )


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
    refresh_total_spending()

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
            refresh_total_spending()

    else:
        messagebox.showerror("Error", "Please select an expense to delete")


root = tk.Tk()

root.title("Expense Tracker")
root.geometry("1100x700")
root.minsize(1000, 650)
root.configure(bg="#f4f6f8")

total_spending_var = tk.StringVar()
total_spending_var.set("Total Spending: ₹0.00")

header_frame = tk.Frame(root, bg="#f4f6f8")
header_frame.pack(fill="x", padx=30, pady=(20, 10))

title_frame = tk.Frame(header_frame, bg="#f4f6f8")
title_frame.pack(side="left")

heading = tk.Label(
    title_frame,
    text="Expense Tracker",
    font=("Arial", 24, "bold"),
    bg="#f4f6f8",
)
heading.pack(anchor="w")

subtitle = tk.Label(
    title_frame,
    text="Track Smarter. Spend Better.",
    font=("Arial", 11),
    bg="#f4f6f8",
)
subtitle.pack(anchor="w")

total_spending_label = tk.Label(
    header_frame,
    textvariable=total_spending_var,
    font=("Arial", 18, "bold"),
    bg="#f4f6f8",
)

total_spending_label.pack(side="right", padx=20)

main_frame = tk.Frame(root)
main_frame.pack(fill="x", padx=30, pady=10)

left_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid",
)

right_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid",
)


left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
right_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=10,
)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

form_heading = tk.Label(
    left_frame,
    text="Expense Details",
    font=("Arial", 14, "bold"),
    bg="white",
)
form_heading.pack(pady=(15, 10))
form_frame = tk.Frame(left_frame, bg="white")
form_frame.pack(padx=30, pady=10)

tools_heading = tk.Label(
    right_frame,
    text="Search & Filter",
    font=("Arial", 14, "bold"),
    bg="white",
)
tools_heading.pack(pady=(15, 10))

search_frame = tk.Frame(
    right_frame,
    bg="white",
)

search_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15),
)

reports_frame = tk.Frame(
    main_frame,
    bg="white",
    bd=1,
    relief="solid",
)

reports_frame.grid(
    row=0,
    column=2,
    sticky="nsew",
    padx=(10, 0),
)

reports_heading = tk.Label(
    reports_frame,
    text="Reports",
    font=("Arial", 14, "bold"),
    bg="white",
)

reports_heading.pack(pady=(0, 10))

date_label = tk.Label(
    form_frame,
    text="Date (YYYY-MM-DD):",
    bg="white",
)
date_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

date_entry = tk.Entry(form_frame, width=30)
date_entry.grid(row=0, column=1, padx=10, pady=8)

category_label = tk.Label(
    form_frame,
    text="Category:",
    bg="white",
)
category_label.grid(row=1, column=0, padx=10, pady=8, sticky="w")

category_var = tk.StringVar()
category_var.set("Food")

filter_category_dropdown = tk.OptionMenu(
    search_frame,
    category_var,
    "All Categories",
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other",
)

filter_category_dropdown.grid(
    row=2,
    column=1,
    padx=10,
    pady=8,
    sticky="ew",
)

amount_label = tk.Label(
    form_frame,
    text="Amount:",
    bg="white",
)
amount_label.grid(row=2, column=0, padx=10, pady=8, sticky="w")

amount_entry = tk.Entry(form_frame, width=30)
amount_entry.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

description_label = tk.Label(
    form_frame,
    text="Description (Optional):",
    bg="white",
)
description_label.grid(row=3, column=0, padx=10, pady=8, sticky="w")

description_entry = tk.Entry(form_frame, width=30)
description_entry.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

add_button = tk.Button(
    form_frame,
    text="Add Expense",
    command=handle_add_expense,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=6,
)

add_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=(15, 10),
)


search_label = tk.Label(
    search_frame,
    text="Search Expense by ID:",
    bg="white",
)
search_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="w",
)

search_entry = tk.Entry(search_frame, width=15)
search_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8,
)

search_button = tk.Button(
    search_frame,
    text="Search Expense",
    command=handle_search_expense,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=4,
)
search_button.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=(5, 10),
)

filter_category_label = tk.Label(
    search_frame,
    text="Filter by Category:",
    bg="white",
)
filter_category_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="w",
)

filter_category_var = tk.StringVar()
filter_category_var.set("All Categories")

category_dropdown = tk.OptionMenu(
    form_frame,
    category_var,
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other",
)


category_dropdown.grid(
    row=1,
    column=1,
    padx=10,
    pady=8,
    sticky="ew",
)

filter_category_button = tk.Button(
    search_frame,
    text="Filter Category",
    command=handle_filter_category,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=4,
)
filter_category_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=(5, 10),
)

filter_date_label = tk.Label(
    search_frame,
    text="Date:",
    bg="white",
)
filter_date_label.grid(
    row=4,
    column=0,
    padx=10,
    pady=8,
    sticky="w",
)

filter_date_entry = tk.Entry(search_frame, width=15)
filter_date_entry.grid(
    row=4,
    column=1,
    padx=10,
    pady=8,
)

filter_date_button = tk.Button(
    search_frame,
    text="Filter Date",
    command=handle_filter_date,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=4,
)
filter_date_button.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=(5, 10),
)

total_button = tk.Button(
    reports_frame,
    text="Spending Summary",
    command=handle_total_spending,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=4,
)
total_button.pack(pady=5)

category_spending_button = tk.Button(
    reports_frame,
    text="Show Category Spending",
    command=handle_category_spending,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=4,
)
category_spending_button.pack(pady=5)

columns = ("ID", "Date", "Category", "Amount", "Description")

table_frame = tk.Frame(root)
table_frame.pack(fill="x", padx=30, pady=10)

# view_button = tk.Button(
#     table_frame,
#     text="View Expenses",
#     command=handle_view_expenses,
# )
# view_button.pack(pady=(0, 5))


records_header = tk.Frame(table_frame)
records_header.pack(fill="x", pady=(0, 8))

records_heading = tk.Label(
    records_header,
    text="Expense Records",
    font=("Arial", 14, "bold"),
)
records_heading.pack(side="left")

show_all_button = tk.Button(
    records_header,
    text="Show All",
    command=handle_view_expenses,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=4,
)
show_all_button.pack(side="right")

tree_frame = tk.Frame(table_frame)
tree_frame.pack(fill="x")

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

expense_table.pack(side="left", fill="x", expand=True)
scrollbar.pack(side="right", fill="y")


action_frame = tk.Frame(root)
action_frame.pack(fill="x", padx=30, pady=(5, 10))

edit_button = tk.Button(
    action_frame,
    text="Edit Selected",
    command=handle_edit_expense,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=5,
)
edit_button.pack(side="left", padx=(0, 10))

update_button = tk.Button(
    action_frame,
    text="Update Expense",
    command=handle_update_expense,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=5,
)
update_button.pack(side="left", padx=10)

delete_button = tk.Button(
    action_frame,
    text="Delete Selected",
    command=handle_delete_expense,
    bg="#dc2626",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=5,
)
delete_button.pack(side="left", padx=10)

handle_view_expenses()
refresh_total_spending()

root.mainloop()
