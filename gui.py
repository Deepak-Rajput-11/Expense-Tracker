import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import date
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    get_expense_dataframe,
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
        refresh_report_stats()
        refresh_category_chart()

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


def handle_filter():
    category = filter_category_var.get()

    if category != "All Categories":
        handle_filter_category()
    else:
        handle_filter_date()


def handle_clear_filter():
    search_entry.delete(0, tk.END)
    filter_category_var.set("All Categories")
    filter_date_entry.set_date(date.today())

    handle_view_expenses()


def handle_export_report():
    df = get_expense_dataframe()

    if df.empty:
        messagebox.showinfo(
            "No Data",
            "No expenses available to export",
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        initialfile="Expense_Report.xlsx",
        title="Save Expense Report",
    )

    if not file_path:
        return

    df.to_excel(
        file_path,
        index=False,
    )

    messagebox.showinfo(
        "Success",
        "Expense report exported successfully",
    )


def refresh_total_spending():
    total = total_spending()
    total_spending_var.set(f"Overall Spending: ₹{total:.2f}")
    return total


def refresh_report_stats():
    total = total_spending()
    highest_category = highest_spending_category()
    count = expense_count()

    report_total_var.set(f"₹{total:.2f}")
    report_category_var.set(highest_category)
    report_count_var.set(str(count))


def refresh_category_chart():
    category_totals = category_wise_spending()

    category_axis.clear()

    if category_totals.empty:
        category_axis.text(
            0.5,
            0.5,
            "No expense data",
            ha="center",
            va="center",
        )
        category_axis.set_axis_off()

    else:
        category_axis.set_axis_on()

        categories = category_totals.index
        amounts = category_totals.values

        total = amounts.sum()

        legend_labels = [
            f"{category}  {amount / total * 100:.1f}%"
            for category, amount in zip(categories, amounts)
        ]

        wedges, texts = category_axis.pie(
            amounts,
            startangle=90,
        )

        category_axis.legend(
            wedges,
            legend_labels,
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=False,
            fontsize=8,
        )

        category_axis.axis("equal")

    category_figure.subplots_adjust(
        left=0.05,
        right=0.68,
        top=0.95,
        bottom=0.08,
    )

    category_canvas.draw()


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


def handle_edit_expense(event=None):
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


def handle_clear_form():
    global editing_expense_id

    editing_expense_id = None

    date_entry.set_date(date.today())
    category_var.set("Food")

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    date_entry.focus()


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
    refresh_report_stats()
    refresh_category_chart()
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

            handle_view_expenses()
            refresh_total_spending()
            refresh_report_stats()
            refresh_category_chart()
            handle_clear_form()

            messagebox.showinfo(
                "Success",
                "Expense deleted successfully",
            )

    else:
        messagebox.showerror(
            "Error",
            "Please select an expense to delete",
        )


root = tk.Tk()

root.title("Expense Tracker")
root.geometry("1100x700")
root.minsize(1000, 650)
root.configure(bg="#f4f6f8")

total_spending_var = tk.StringVar()
total_spending_var.set("Total Spending: ₹0.00")

report_total_var = tk.StringVar()
report_total_var.set("₹0.00")

report_category_var = tk.StringVar()
report_category_var.set("No Data")

report_count_var = tk.StringVar()
report_count_var.set("0")

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

header_stats_frame = tk.Frame(
    header_frame,
    bg="#f4f6f8",
)

header_stats_frame.pack(
    side="right",
    padx=20,
)

total_spending_label = tk.Label(
    header_stats_frame,
    textvariable=total_spending_var,
    font=("Arial", 18, "bold"),
    bg="#f4f6f8",
)

total_spending_label.pack(
    anchor="e",
)

today_label = tk.Label(
    header_stats_frame,
    text=f"Today: {date.today().strftime('%d %b %Y')}",
    font=("Arial", 10),
    bg="#f4f6f8",
)

today_label.pack(
    anchor="e",
    pady=(3, 0),
)

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
    text="Add / Edit Expense",
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
search_frame.columnconfigure(0, weight=1)
search_frame.columnconfigure(1, weight=1)
search_frame.columnconfigure(2, weight=1)

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

report_stats_frame = tk.Frame(
    reports_frame,
    bg="white",
)

report_stats_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 10),
)

report_total_label = tk.Label(
    report_stats_frame,
    text="Total Spending",
    font=("Arial", 9),
    bg="white",
)

report_total_label.pack(anchor="w")

report_total_value = tk.Label(
    report_stats_frame,
    textvariable=report_total_var,
    font=("Arial", 12, "bold"),
    bg="white",
)

report_total_value.pack(anchor="w", pady=(0, 8))

report_category_label = tk.Label(
    report_stats_frame,
    text="Highest Category",
    font=("Arial", 9),
    bg="white",
)

report_category_label.pack(anchor="w")

report_category_value = tk.Label(
    report_stats_frame,
    textvariable=report_category_var,
    font=("Arial", 12, "bold"),
    bg="white",
)

report_category_value.pack(anchor="w", pady=(0, 8))

report_count_label = tk.Label(
    report_stats_frame,
    text="Total Expenses",
    font=("Arial", 9),
    bg="white",
)

report_count_label.pack(anchor="w")

report_count_value = tk.Label(
    report_stats_frame,
    textvariable=report_count_var,
    font=("Arial", 12, "bold"),
    bg="white",
)

report_count_value.pack(anchor="w")

date_label = tk.Label(
    form_frame,
    text="Date (YYYY-MM-DD):",
    bg="white",
)
date_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

date_entry = DateEntry(
    form_frame,
    width=27,
    date_pattern="yyyy-mm-dd",
    font=("Arial", 9),
)
date_entry.grid(row=0, column=1, padx=10, pady=8)

category_label = tk.Label(
    form_frame,
    text="Category:",
    bg="white",
)
category_label.grid(row=1, column=0, padx=10, pady=8, sticky="w")

category_var = tk.StringVar()
category_var.set("Food")

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

form_button_frame = tk.Frame(
    form_frame,
    bg="white",
)

form_button_frame.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="ew",
    padx=10,
    pady=(15, 10),
)

form_button_frame.columnconfigure(0, weight=1)
form_button_frame.columnconfigure(1, weight=1)
form_button_frame.columnconfigure(2, weight=1)

add_button = tk.Button(
    form_button_frame,
    text="Add Expense",
    command=handle_add_expense,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=6,
)

add_button.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(0, 5),
)

clear_form_button = tk.Button(
    form_button_frame,
    text="Clear Form",
    command=handle_clear_form,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=6,
)

clear_form_button.grid(
    row=0,
    column=2,
    sticky="ew",
    padx=(5, 0),
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
    text="Search",
    command=handle_search_expense,
    bg="#16a34a",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=6,
)

search_button.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=(10, 5),
    pady=(12, 5),
)

filter_button = tk.Button(
    search_frame,
    text="Filter",
    command=handle_filter,
    bg="#9333ea",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=6,
)

filter_button.grid(
    row=3,
    column=1,
    sticky="ew",
    padx=5,
    pady=(12, 5),
)

clear_filter_button = tk.Button(
    search_frame,
    text="Clear Filter",
    command=handle_clear_filter,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=6,
)

clear_filter_button.grid(
    row=3,
    column=2,
    sticky="ew",
    padx=(5, 10),
    pady=(12, 5),
)

filter_category_label = tk.Label(
    search_frame,
    text="Filter by Category:",
    bg="white",
)

filter_category_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=6,
    sticky="w",
)

filter_category_var = tk.StringVar()
filter_category_var.set("All Categories")

filter_category_dropdown = tk.OptionMenu(
    search_frame,
    filter_category_var,
    "All Categories",
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other",
)

filter_category_dropdown.config(width=14)

filter_category_dropdown.grid(
    row=1,
    column=1,
    padx=10,
    pady=6,
    sticky="ew",
)


filter_date_label = tk.Label(
    search_frame,
    text="Date:",
    bg="white",
)
filter_date_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=6,
    sticky="w",
)

filter_date_entry = DateEntry(
    search_frame,
    width=12,
    date_pattern="yyyy-mm-dd",
    font=("Arial", 9),
)
filter_date_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=6,
    sticky="ew",
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

export_button = tk.Button(
    reports_frame,
    text="Export Report",
    command=handle_export_report,
    bg="#16a34a",
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=4,
)

export_button.pack(pady=5)

lower_frame = tk.Frame(
    root,
    bg="#f4f6f8",
)

lower_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10,
)

lower_frame.columnconfigure(0, weight=3)
lower_frame.columnconfigure(1, weight=2)
lower_frame.rowconfigure(0, weight=1)


columns = ("ID", "Date", "Category", "Amount", "Description")

table_frame = tk.Frame(
    lower_frame,
    bg="white",
    bd=1,
    relief="solid",
)

table_frame.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 10),
)

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

tree_frame = tk.Frame(table_frame)
tree_frame.pack(fill="x")

expense_table = ttk.Treeview(
    tree_frame,
    columns=columns,
    show="headings",
    height=6,
    selectmode="browse",
)
expense_table.bind(
    "<Double-1>",
    handle_edit_expense,
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


action_frame = tk.Frame(
    table_frame,
    bg="white",
)

action_frame.pack(
    fill="x",
    padx=15,
    pady=(10, 15),
)

update_button = tk.Button(
    form_button_frame,
    text="Update Expense",
    command=handle_update_expense,
    bg="#f59e0b",
    fg="black",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=10,
    pady=6,
)

update_button.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=5,
)

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

view_all_button = tk.Button(
    action_frame,
    text="View All",
    command=handle_view_expenses,
    bg="#e5e7eb",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=5,
)

view_all_button.pack(side="left", padx=10)

chart_frame = tk.Frame(
    lower_frame,
    bg="white",
    bd=1,
    relief="solid",
)

chart_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(10, 0),
)


chart_heading = tk.Label(
    chart_frame,
    text="Category Spending",
    font=("Arial", 14, "bold"),
    bg="white",
)

chart_heading.pack(
    anchor="w",
    padx=20,
    pady=(15, 10),
)


category_figure = Figure(
    figsize=(4, 3),
    dpi=100,
)

category_axis = category_figure.add_subplot(111)

category_canvas = FigureCanvasTkAgg(
    category_figure,
    master=chart_frame,
)

category_canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10),
)


handle_view_expenses()
refresh_total_spending()
refresh_report_stats()
refresh_category_chart()

root.mainloop()
