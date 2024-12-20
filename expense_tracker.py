import sqlite3
import calendar
import datetime
from termcolor import colored
from expense import Expense

def main():
    print(f"🎯 Running Expense Tracker!")
    budget=10000

    create_db()
    # Get user input for expense.
    expense = get_user_expense()
    
    # Write their expense to a file.
    save_expense_to_db(expense)
        
    # Read file and Summarize expense.
    summarize_expenses(budget)

def create_db():
    print(f"🎯 Setting up the database...")
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏡 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc"
    ]
    
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")
        
        value_range = f"[1 -{len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
              
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again!")  
        
def save_expense_to_db(expense: Expense):
    print(f"🎯 Saving User Expense: {expense} to the database")
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (name, amount, category)
        VALUES (?, ?, ?)
    ''', (expense.name, expense.amount, expense.category))
    conn.commit()
    conn.close()

def summarize_expenses(budget):
    print(f"🎯 Summarizing User Expense")
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()

    expenses = []
    for row in rows:
        expense = Expense(name=row[1], amount=row[2], category=row[3])
        expenses.append(expense)

    conn.close()

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expense By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f" {key}: ₹{amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💸 You've spent ₹{total_spent:.2f} this month!")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ₹{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ₹{daily_budget:.2f}"))

def green(text):
    return colored(text, 'green')
            
if __name__ =="__main__":
    main()
    