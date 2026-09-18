from datetime import datetime, date


def validate_amount(amount):
    if amount == "":
        return False

    try:
        amount = float(amount)
    except ValueError:
        return False

    if amount <= 0:
        return False

    return True


def validate_category(category):
    categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]

    if category in categories:
        return True

    return False


def validate_date(expense_date):
    if expense_date == "":
        return False

    try:
        entered_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
    except ValueError:
        return False

    if entered_date > date.today():
        return False

    return True
