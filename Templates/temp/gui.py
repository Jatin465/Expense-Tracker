import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:5000/expenses"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expense_list = tk.Listbox(root, width=50, height=20)
        self.expense_list.pack()

        self.expense_entry = tk.Entry(root)
        self.expense_entry.pack()

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.update_button = tk.Button(root, text="Update Expense", command=self.update_expense)
        self.update_button.pack()

        self.delete_button = tk.Button(root, text="Delete Expense", command=self.delete_expense)
        self.delete_button.pack()

        self.load_expenses()

    def load_expenses(self):
        response = requests.get(API_URL)
        if response.status_code == 200:
            expenses = response.json()
            self.expense_list.delete(0, tk.END)
            for expense in expenses:
                self.expense_list.insert(tk.END, f"{expense['_id']}: {expense['description']} - ${expense['amount']}")

    def add_expense(self):
        description = self.expense_entry.get()
        amount = 100  # Placeholder amount
        expense = {"description": description, "amount": amount}
        response = requests.post(API_URL, json=expense)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Expense added successfully!")
            self.load_expenses()
        else:
            messagebox.showerror("Error", "Failed to add expense.")

    def update_expense(self):
        selected = self.expense_list.curselection()
        if selected:
            expense_id = self.expense_list.get(selected[0]).split(":")[0]
            new_description = self.expense_entry.get()
            new_amount = 150  # Placeholder updated amount
            update = {"description": new_description, "amount": new_amount}
            response = requests.put(f"{API_URL}/{expense_id}", json=update)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Expense updated successfully!")
                self.load_expenses()
            else:
                messagebox.showerror("Error", "Failed to update expense.")
        else:
            messagebox.showerror("Error", "No expense selected.")

    def delete_expense(self):
        selected = self.expense_list.curselection()
        if selected:
            expense_id = self.expense_list.get(selected[0]).split(":")[0]
            response = requests.delete(f"{API_URL}/{expense_id}")
            if response.status_code == 200:
                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.load_expenses()
            else:
                messagebox.showerror("Error", "Failed to delete expense.")
        else:
            messagebox.showerror("Error", "No expense selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
