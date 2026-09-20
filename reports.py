import pandas as pd
from database import view_expenses


def get_expense_dataframe():
    expenses = view_expenses()

    df = pd.DataFrame(
        expenses, columns=["expense_id", "date", "category", "amount", "description"]
    )

    return df


def total_spending():
    df = get_expense_dataframe()

    total = df["amount"].sum()

    return total


def category_wise_spending():
    df = get_expense_dataframe()

    category_totals = df.groupby("category")["amount"].sum()

    return category_totals
