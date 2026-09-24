# Expense Tracker

A desktop Expense Tracker application built using Python, Tkinter, SQLite, and Pandas.

The project allows users to manage daily expenses, store them permanently, filter expense records, and analyze spending.

## Features

- Add expenses
- View expenses
- Search expenses by ID
- Update expenses
- Delete expenses
- Filter expenses by category and date
- View total spending
- View category-wise spending

## Day 1 - Project Setup & Database Foundation

- Planned the expense data structure
- Defined validation rules
- Designed the application features
- Created the project structure
- Set up SQLite database
- Created the `expenses` table
- Implemented automatic expense IDs
- Implemented `add_expense()`
- Implemented `view_expenses()`
- Added `.gitignore` for the database file

## Day 2 - Database CRUD Operations

- Implemented search expense by ID
- Used `WHERE` conditions and `fetchone()`
- Implemented update expense functionality
- Implemented delete expense functionality
- Used parameterized SQL queries for database operations
- Tested search, update, and delete operations successfully

## Day 3 - Input Validation

- Created a separate `validation.py` module
- Implemented amount validation
- Added checks for numeric and positive expense amounts
- Implemented predefined category validation
- Implemented date validation using Python `datetime`
- Prevented invalid and future dates
- Tested all validation functions successfully

## Day 4 - Expense Filtering

- Implemented expense filtering by category
- Implemented expense filtering by date
- Used SQL `WHERE` conditions for filtering
- Used `fetchall()` to retrieve multiple matching expense records
- Tested category and date filters successfully

## Day 5 - Spending Reports & Pandas Integration

- Created a separate `reports.py` module
- Integrated Pandas with SQLite expense data
- Converted expense records into a Pandas DataFrame
- Implemented total spending calculation
- Implemented category-wise spending using `groupby()`
- Created a reusable DataFrame helper function to avoid duplicate code
- Tested spending reports successfully

## Day 6 - Backend Integration & Testing

- Integrated database, validation, and reporting modules
- Tested adding and viewing expenses
- Tested searching and updating expenses
- Tested expense deletion
- Tested category and date filters
- Tested total and category-wise spending reports
- Verified invalid expense data is rejected before database insertion
- Confirmed the complete backend workflow is working correctly

## Day 7 - GUI Foundation & Add Expense Integration

- Created a separate `gui.py` module using Tkinter
- Built the main Expense Tracker window
- Created input fields for date, category, amount, and description
- Added a predefined category dropdown
- Connected GUI inputs with existing validation functions
- Connected the Add Expense button with the SQLite database
- Added success and error message boxes
- Added automatic form clearing after successful expense insertion
- Added a View Expenses button and connected it with the database
- Tested GUI-to-database integration successfully

## Day 8 - View Expenses Table

- Added a Treeview table to display expense records in the GUI
- Connected the View Expenses button with the Treeview
- Displayed SQLite expense records in rows and columns
- Added column headings and adjusted column widths
- Prevented duplicate rows when refreshing expense data
- Added a vertical scrollbar for larger expense lists
- Configured the table height for better layout
- Enabled single-row selection for future update and delete operations

## Day 9 - Search & Delete Expense GUI

- Added expense search by ID
- Connected the search feature with the SQLite database
- Displayed searched expenses directly in the Treeview
- Added validation for empty and nonexistent expense searches
- Added single-row expense deletion from the Treeview
- Retrieved the database expense ID from the selected table row
- Added delete confirmation before removing an expense
- Added success and error message boxes for deletion
- Automatically refreshed the expense table after deletion

## Technologies Used

- Python
- Tkinter
- SQLite
- Pandas
- Git & GitHub

## Project Status

🚧 In Progress
