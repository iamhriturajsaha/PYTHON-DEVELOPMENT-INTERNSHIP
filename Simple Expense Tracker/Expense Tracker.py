# 📌 SIMPLE EXPENSE TRACKER

# 🎯 Project Goals -
#  - Track personal expenses in different categories.
#  - Provide total and category-wise expense reports.
#  - Keep the program user-friendly, scalable and error-free.

# Features Implemented -
# 1. Add expenses with category and amount.
# 2. View total expenses.
# 3. View expenses by category.
# 4. Exit with a final summary report.
# 5. Password login.
# 6. Budget alerts if category spending exceeds limit.

import sys
# Configuration
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Others"]
# Default budget set for each category
BUDGETS = {category: 5000 for category in CATEGORIES}
# Password for login
PASSWORD = "1234"
# List to store all expenses as dictionaries
expenses = []
# Helper Functions
def login():
    """
    Simple login system with password protection.
    - Allows 3 attempts before exiting.
    - Helps protect personal expense data.
    """
    for attempt in range(3):
        pwd = input("🔑 Enter password (or 'q' to quit): ")
        if pwd.lower() == "q":  # Allow user to quit instead of retrying
            print("❌ Exiting...")
            sys.exit()
        if pwd == PASSWORD:
            print("✅ Login successful!\n")
            return  # Exit function and continue program
        else:
            print("⚠️ Incorrect password, try again.")
    # If all 3 attempts fail, exit program
    print("❌ Too many failed attempts. Exiting.")
    sys.exit()
def add_expense():
    """
    Add a new expense:
    - User selects category from menu.
    - User enters expense amount.
    - Expense is stored in global list.
    - Alerts if budget limit exceeded.
    """
    print("\n📌 Available categories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}. {cat}")
    try:
        choice = int(input("Select a category number: "))
        # Validate category choice
        if choice < 1 or choice > len(CATEGORIES):
            print("⚠️ Invalid category choice. Try again.")
            return
        category = CATEGORIES[choice - 1]  # Map number to category name
        # Get expense amount
        amount = float(input(f"Enter amount for {category}: "))
        if amount <= 0:
            print("⚠️ Amount must be greater than zero.")
            return
        # Save expense to list
        expenses.append({"amount": amount, "category": category})
        print(f"✅ Added {amount} under {category}.")
        # Budget alert check
        total_cat = sum(e["amount"] for e in expenses if e["category"] == category)
        if total_cat > BUDGETS[category]:
            print(f"⚠️ ALERT: You exceeded the budget for {category}! (Limit: {BUDGETS[category]})")
    except ValueError:
        # Catch invalid number inputs
        print("⚠️ Invalid input. Please enter numeric values where required.")
def view_total():
    """
    Show total amount spent across all categories.
    """
    total = sum(e["amount"] for e in expenses)
    print(f"\n💰 Total Expenses: {total}")
def view_by_category():
    """
    Show total spending per category.
    Helpful for identifying where money is going.
    """
    print("\n📊 Expenses by Category:")
    for category in CATEGORIES:
        total_cat = sum(e["amount"] for e in expenses if e["category"] == category)
        print(f"{category}: {total_cat}")
def summary_report():
    """
    Display a final report before exit:
    - Total spending
    - Highest spending category
    - Lowest spending category
    """
    print("\n📄 Summary Report:")
    total = sum(e["amount"] for e in expenses)
    print(f"Total spent: {total}")
    if expenses:  # Only run if there are expenses
        # Compute totals for each category
        category_totals = {cat: sum(e["amount"] for e in expenses if e["category"] == cat) for cat in CATEGORIES}
        highest = max(category_totals, key=category_totals.get)
        lowest = min(category_totals, key=category_totals.get)
        print(f"Highest spending: {highest} ({category_totals[highest]})")
        print(f"Lowest spending: {lowest} ({category_totals[lowest]})")
    else:
        print("No expenses recorded.")
def main_menu():
    """
    Main program loop:
    - Displays menu
    - Handles user input
    - Calls appropriate functions
    """
    while True:
        print("\n====== Expense Tracker Menu ======")
        print("1. Add Expense")
        print("2. View Total Expenses")
        print("3. View Expenses by Category")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_total()
        elif choice == "3":
            view_by_category()
        elif choice == "4":
            # Show summary before quitting
            summary_report()
            print("👋 Thank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please enter 1-4.")
# Program Entry Point
if __name__ == "__main__":
    print("🔒 Welcome to Expense Tracker")
    login()       # Ask for password before accessing tracker
    main_menu()   # Start the main loop
