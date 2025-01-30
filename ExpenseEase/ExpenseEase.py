import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Import ttk for themed widgets
from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class Transaction:
    def __init__(self, date, amount, category, description=""):
        self.date = datetime.strptime(date, "%Y-%m-%d").date() if isinstance(date, str) else date
        self.amount = amount
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", "")
        )

class ExpenseTracker:
    CATEGORY_POINTS = 5

    def __init__(self, data_file="transactions.json"):
        self.transactions = []
        self.recurring_expenses = []
        self.total_points = 0
        self.data_file = data_file
        self.load_data()
        self.process_recurring_expenses()
        self.badges = []

    def validate_transaction_data(self, date, amount, category):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return False

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be a positive number.")
            return False

        if not category.strip():
            messagebox.showerror("Error", "Category cannot be empty.")
            return False

        return True
    
    def add_transaction(self, date, amount, category, description=""):
        transaction = Transaction(date, amount, category, description)
        self.transactions.append(transaction)
        self.total_points += self.CATEGORY_POINTS
        self.award_badges()
        self.save_data()

    def award_badges(self):
        # Starter Saver: Awarded after the first transaction
        if self.total_points >= 5 and "Starter Saver" not in self.badges:
            self.badges.append("Starter Saver")
            messagebox.showinfo("New Badge!", "Congratulations! You earned the 'Starter Saver' badge.")

        # Transaction Master: Awarded after 10 transactions
        if len(self.transactions) >= 10 and "Transaction Master" not in self.badges:
            self.badges.append("Transaction Master")
            messagebox.showinfo("New Badge!", "Congratulations! You earned the 'Transaction Master' badge.")

        # Big Spender: Total amount spent >= $1,000
        if sum(t.amount for t in self.transactions) >= 1000 and "Big Spender" not in self.badges:
            self.badges.append("Big Spender")
            messagebox.showinfo("New Badge!", "Congratulations! You earned the 'Big Spender' badge.")

        # Frequent User: Awarded after 30 transactions
        if len(self.transactions) >= 30 and "Frequent User" not in self.badges:
            self.badges.append("Frequent User")
            messagebox.showinfo("New Badge!", "Congratulations! You earned the 'Frequent User' badge.")

        self.save_data()

    def add_recurring_expense(self, amount, category, description, frequency, next_due_date):
        recurring_expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "frequency": frequency,
            "next_due_date": next_due_date.strftime("%Y-%m-%d"),
            "status": "Upcoming"
        }
        self.recurring_expenses.append(recurring_expense)
        self.save_data()

    def process_recurring_expenses(self):
        today = datetime.today().date()
        for expense in self.recurring_expenses:
            next_due_date = datetime.strptime(expense["next_due_date"], "%Y-%m-%d").date()
            while next_due_date <= today:
                self.add_transaction(next_due_date, expense["amount"], expense["category"], expense["description"])
                expense["status"] = "Processed"
                next_due_date = self.calculate_next_due_date(next_due_date, expense["frequency"])
                expense["next_due_date"] = next_due_date.strftime("%Y-%m-%d")
        self.save_data()

    def calculate_next_due_date(self, current_date, frequency):
        if frequency == "Daily":
            return current_date + timedelta(days=1)
        elif frequency == "Weekly":
            return current_date + timedelta(weeks=1)
        elif frequency == "Monthly":
            return current_date + timedelta(days=30)
        return current_date

    def save_data(self):
        with open(self.data_file, "w") as file:
            data = {
                "transactions": [t.to_dict() for t in self.transactions],
                "recurring_expenses": self.recurring_expenses,
                "total_points": self.total_points,
                "badges": self.badges
            }
            json.dump(data, file)

    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
                self.recurring_expenses = data.get("recurring_expenses", [])
                self.total_points = data.get("total_points", 0)
                self.badges = data.get("badges", [])
        except FileNotFoundError:
            self.transactions = []
            self.recurring_expenses = []
            self.total_points = 0
            self.badges = []
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
            self.transactions = []
            self.recurring_expenses = []
            self.total_points = 0
            self.badges = []

    def get_category_totals(self):
        category_totals = defaultdict(float)
        for transaction in self.transactions:
            category_totals[transaction.category] += transaction.amount
        return category_totals

    def display_visualizations(self):
        category_totals = self.get_category_totals()
        if not category_totals:
            messagebox.showinfo("Expense Analytics", "No transactions to analyze.")
            return

        categories = list(category_totals.keys())
        totals = list(category_totals.values())

        # Bar Chart
        plt.figure(figsize=(10, 5))
        plt.bar(categories, totals, color="skyblue")
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Pie Chart
        plt.figure(figsize=(8, 8))
        plt.pie(totals, labels=categories, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
        plt.title("Spending Distribution")
        plt.tight_layout()
        plt.show()

class ExpenseApp(tk.Tk):
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.title("ExpenseEase - SpendTrack")
        self.geometry("600x450")
        self.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        tk.Label(self, text="ExpenseEase - SpendTrack", font=("Helvetica", 20, "bold"), bg="#f0f0f0",
                 fg="#333333").pack(pady=10)

        # Main Frame with Grid Layout
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Button Frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0", padx=20)
        button_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Use ttk.Button for consistent appearance
        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 12), padding=10)

        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction_dialog).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(button_frame, text="Add Recurring Expense", command=self.add_recurring_expense_dialog).grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(button_frame, text="Spending Summary", command=self.display_spending_summary).grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(button_frame, text="Check Points & Badges", command=self.show_points_and_badges).grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(button_frame, text="View Recurring Expenses", command=self.show_recurring_expenses).grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(button_frame, text="Edit Transaction", command=self.edit_transaction_dialog).grid(row=5, column=0,padx=10, pady=10,sticky="ew")

        # Transactions Listbox
        self.transaction_list = tk.Listbox(main_frame, height=15, width=70, bg="white", fg="#333333",
                                           font=("Helvetica", 11))
        self.transaction_list.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        # Adjust the row and column weights for responsive resizing
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        self.refresh_transactions()

    def show_points_and_badges(self):
        points_message = f"You currently have {self.tracker.total_points} points.\n\n"
        badges_message = f"Badges Earned: {', '.join(self.tracker.badges) if self.tracker.badges else 'No badges yet.'}"
        messagebox.showinfo("Points and Badges", points_message + badges_message)

    def display_spending_summary(self):
        # Calculate summaries
        category_totals = self.tracker.get_category_totals()
        total_spent = sum(transaction.amount for transaction in self.tracker.transactions)
        num_transactions = len(self.tracker.transactions)

        summary_window = tk.Toplevel(self)
        summary_window.title("Spending Summary")
        summary_window.geometry("600x400")

        tk.Label(summary_window, text=f"Total Transactions: {num_transactions}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(summary_window, text=f"Total Spent: ${total_spent:.2f}", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(summary_window, text=f"Total Points: {self.tracker.total_points}", font=("Helvetica", 14)).pack(
            pady=10)

        # Display per-category summary
        category_frame = tk.Frame(summary_window)
        category_frame.pack(pady=10)

        tk.Label(category_frame, text="Category Breakdown:", font=("Helvetica", 12, "bold")).pack()
        for category, total in category_totals.items():
            num_category_transactions = sum(1 for t in self.tracker.transactions if t.category == category)
            tk.Label(category_frame, text=f"{category}: ${total:.2f} ({num_category_transactions} transactions)").pack(
                anchor="w")

        # Add visualization button in the summary window
        tk.Button(summary_window, text="Show Spending Chart", command=self.tracker.display_visualizations).pack(pady=20)

    def refresh_transactions(self):
        self.transaction_list.delete(0, tk.END)
        for transaction in self.tracker.transactions:
            # Now including the description in the list box
            description = transaction.description if transaction.description else "No description"
            self.transaction_list.insert(tk.END, f"{transaction.date} | {transaction.category} | ${transaction.amount:.2f} | {description}")

    def add_transaction_dialog(self):
        # Create a new window (dialog)
        dialog = tk.Toplevel(self)
        dialog.title("Add Transaction")
        dialog.geometry("400x300")

        # Labels and entry fields for each input
        tk.Label(dialog, text="Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(dialog)
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))  # Default to today's date

        tk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(dialog)
        amount_entry.pack(pady=5)

        tk.Label(dialog, text="Category:").pack(pady=5)
        category_entry = tk.Entry(dialog)
        category_entry.pack(pady=5)

        tk.Label(dialog, text="Description (optional):").pack(pady=5)
        description_entry = tk.Entry(dialog)
        description_entry.pack(pady=5)

        # Function to collect data and close dialog
        def submit_transaction():
            date = date_entry.get()
            try:
                amount = float(amount_entry.get())
                category = category_entry.get()
                description = description_entry.get()

                self.tracker.add_transaction(date, amount, category, description)
                messagebox.showinfo("Success",
                                    f"Transaction added successfully!\nYou earned {self.tracker.CATEGORY_POINTS} points.")
                self.refresh_transactions()
                dialog.destroy()  # Close the dialog
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered. Please try again.")

        # Submit button
        tk.Button(dialog, text="Add Transaction", command=submit_transaction).pack(pady=20)

    def add_recurring_expense_dialog(self):
        try:
            amount = float(simpledialog.askstring("Input", "Enter the recurring expense amount:"))
            category = simpledialog.askstring("Input", "Enter the category (e.g., Rent, Gas, etc.):")
            description = simpledialog.askstring("Input", "Enter a description (optional):")
            frequency = simpledialog.askstring("Input", "Enter the frequency (Daily, Weekly, Monthly):")
            next_due_date_str = simpledialog.askstring("Input", "Enter the next due date (YYYY-MM-DD):")
            next_due_date = datetime.strptime(next_due_date_str, "%Y-%m-%d")

            self.tracker.add_recurring_expense(amount, category, description, frequency, next_due_date)
            messagebox.showinfo("Success", "Recurring expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def show_points(self):
        messagebox.showinfo("Total Points", f"You currently have {self.tracker.total_points} points.")

    def show_recurring_expenses(self):
        # Open a new window to display recurring expenses
        expense_window = tk.Toplevel(self)
        expense_window.title("Recurring Expenses")
        expense_window.geometry("600x400")

        # Create a Listbox to display recurring expenses
        listbox = tk.Listbox(expense_window, width=80, height=15)
        listbox.pack(padx=10, pady=10)

        # Check if there are any recurring expenses
        if not self.tracker.recurring_expenses:
            listbox.insert(tk.END, "No recurring expenses found.")
        else:
            for expense in self.tracker.recurring_expenses:
                # Debugging: print the expense to check its structure
                print(expense)  # This will help identify the structure of each expense

                # Safely access the fields using .get() to avoid KeyError if a field is missing
                category = expense.get('category', 'N/A')
                amount = expense.get('amount', 0.0)
                next_due_date = expense.get('next_due_date', 'N/A')
                status = expense.get('status', 'N/A')

                # Format the string to display in the listbox
                expense_info = f"{category} | ${amount:.2f} | Next Due: {next_due_date} | Status: {status}"
                listbox.insert(tk.END, expense_info)

    def edit_transaction_dialog(self):
        # Get selected transaction
        selected_index = self.transaction_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a transaction to edit.")
            return

        selected_transaction = self.tracker.transactions[selected_index[0]]

        # Create a new window (dialog)
        dialog = tk.Toplevel(self)
        dialog.title("Edit Transaction")
        dialog.geometry("400x300")

        # Pre-fill fields with the existing transaction data
        tk.Label(dialog, text="Date (YYYY-MM-DD):").pack(pady=5)
        date_entry = tk.Entry(dialog)
        date_entry.pack(pady=5)
        date_entry.insert(0, selected_transaction.date.strftime("%Y-%m-%d"))

        tk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(dialog)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, str(selected_transaction.amount))

        tk.Label(dialog, text="Category:").pack(pady=5)
        category_entry = tk.Entry(dialog)
        category_entry.pack(pady=5)
        category_entry.insert(0, selected_transaction.category)

        tk.Label(dialog, text="Description (optional):").pack(pady=5)
        description_entry = tk.Entry(dialog)
        description_entry.pack(pady=5)
        description_entry.insert(0, selected_transaction.description)

        # Function to update the transaction and close dialog
        def submit_edit():
            try:
                selected_transaction.date = datetime.strptime(date_entry.get(), "%Y-%m-%d").date()
                selected_transaction.amount = float(amount_entry.get())
                selected_transaction.category = category_entry.get()
                selected_transaction.description = description_entry.get()

                self.tracker.save_data()  # Save updated data to file
                self.refresh_transactions()  # Refresh the listbox
                messagebox.showinfo("Success", "Transaction updated successfully!")
                dialog.destroy()  # Close the dialog
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please try again.")

        # Submit button
        tk.Button(dialog, text="Update Transaction", command=submit_edit).pack(pady=20)

if __name__ == "__main__":
    tracker = ExpenseTracker()  # Create an instance of ExpenseTracker
    app = ExpenseApp(tracker)  # Pass the tracker to the ExpenseApp
    app.mainloop()  # Start the Tkinter event loop
