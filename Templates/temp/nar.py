from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
db = PyMongo(app).db

@app.route("/")
def home():
    db.inventory.insert_one({"b":1})
    return "<p>Home</p>"

if __name__ == '__main__':
    app.run(debug=True)


# #Rest API
# '''1. Get, 2. Post, 3. Put, 4. Patch, 5. Delete'''
# from flask import Flask,render_template,request

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")
# @app.route("/id",methods=["GET","POST"])
# def id():
#     name = None
#     password = None
#     if request.method == 'POST':
#         name = request.form.get('name')
#         password = request.form.get('password')
#     return render_template("result.html",name=name,password=password)

# @app.route("/login")
# def login():
#     return "<p>Shift to New Page</p>"


# if __name__ == '__main__':
#     app.run()


# import tkinter as tk
# from tkinter import messagebox
# import requests

# # API URL for the Flask server
# API_URL = "http://127.0.0.1:5000/expenses"

# class ExpenseTracker:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Expense Tracker")

#         # Frame for the Listbox and Scrollbar
#         frame = tk.Frame(root)
#         frame.pack(pady=20)

#         # Scrollbar for the Listbox
#         scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         # Listbox to display expenses
#         self.expense_list = tk.Listbox(frame, width=50, height=20, yscrollcommand=scrollbar.set)
#         self.expense_list.pack(side=tk.LEFT, fill=tk.BOTH)
#         scrollbar.config(command=self.expense_list.yview)

#         # Entry fields for expense description and amount
#         self.description_entry = tk.Entry(root, width=25)
#         self.description_entry.pack(pady=5)

#         self.amount_entry = tk.Entry(root, width=10)
#         self.amount_entry.pack(pady=5)

#         # Frame for the buttons
#         button_frame = tk.Frame(root)
#         button_frame.pack(pady=10)

#         # Button to add a new expense
#         self.add_button = tk.Button(button_frame, text="Add Expense", command=self.add_expense)
#         self.add_button.grid(row=0, column=0, padx=5)

#         # Button to update an existing expense
#         self.update_button = tk.Button(button_frame, text="Update Expense", command=self.update_expense)
#         self.update_button.grid(row=0, column=1, padx=5)

#         # Button to delete an existing expense
#         self.delete_button = tk.Button(button_frame, text="Delete Expense", command=self.delete_expense)
#         self.delete_button.grid(row=0, column=2, padx=5)

#         # Button to clear the entry fields
#         self.clear_button = tk.Button(button_frame, text="Clear Fields", command=self.clear_fields)
#         self.clear_button.grid(row=0, column=3, padx=5)

#         # Load and display current expenses
#         self.load_expenses()

#     def load_expenses(self):
#         """Load and display all expenses from the Flask server."""
#         response = requests.get(API_URL)
#         if response.status_code == 200:
#             expenses = response.json()
#             self.expense_list.delete(0, tk.END)
#             for expense in expenses:
#                 display_text = f"{expense['description']} - ${expense['amount']}"
#                 self.expense_list.insert(tk.END, display_text)
#         else:
#             messagebox.showerror("Error", "Failed to load expenses.")

#     def add_expense(self):
#         """Add a new expense to the database."""
#         description = self.description_entry.get()
#         try:
#             amount = float(self.amount_entry.get())
#         except ValueError:
#             messagebox.showerror("Error", "Invalid amount. Please enter a number.")
#             return
        
#         expense = {"description": description, "amount": amount}
#         response = requests.post(API_URL, json=expense)
#         if response.status_code == 201:
#             messagebox.showinfo("Success", "Expense added successfully!")
#             self.load_expenses()
#             self.clear_fields()
#         else:
#             messagebox.showerror("Error", "Failed to add expense.")

#     def update_expense(self):
#         """Update the selected expense."""
#         selected = self.expense_list.curselection()
#         if selected:
#             description = self.description_entry.get()
#             try:
#                 amount = float(self.amount_entry.get())
#             except ValueError:
#                 messagebox.showerror("Error", "Invalid amount. Please enter a number.")
#                 return
            
#             expense_id = selected[0]
#             response = requests.get(API_URL)
#             if response.status_code == 200:
#                 expenses = response.json()
#                 selected_expense = expenses[expense_id]
#                 update = {"description": description, "amount": amount}
#                 response = requests.put(f"{API_URL}/{selected_expense['_id']}", json=update)
#                 if response.status_code == 200:
#                     messagebox.showinfo("Success", "Expense updated successfully!")
#                     self.load_expenses()
#                     self.clear_fields()
#                 else:
#                     messagebox.showerror("Error", "Failed to update expense.")
#             else:
#                 messagebox.showerror("Error", "Failed to load expenses.")
#         else:
#             messagebox.showerror("Error", "No expense selected.")

#     def delete_expense(self):
#         """Delete the selected expense."""
#         selected = self.expense_list.curselection()
#         if selected:
#             expense_id = selected[0]
#             response = requests.get(API_URL)
#             if response.status_code == 200:
#                 expenses = response.json()
#                 selected_expense = expenses[expense_id]
#                 response = requests.delete(f"{API_URL}/{selected_expense['_id']}")
#                 if response.status_code == 200:
#                     messagebox.showinfo("Success", "Expense deleted successfully!")
#                     self.load_expenses()
#                     self.clear_fields()
#                 else:
#                     messagebox.showerror("Error", "Failed to delete expense.")
#             else:
#                 messagebox.showerror("Error", "Failed to load expenses.")
#         else:
#             messagebox.showerror("Error", "No expense selected.")

#     def clear_fields(self):
#         """Clear the entry fields."""
#         self.description_entry.delete(0, tk.END)
#         self.amount_entry.delete(0, tk.END)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ExpenseTracker(root)
#     root.mainloop()

