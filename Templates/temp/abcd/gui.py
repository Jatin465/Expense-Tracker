import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Flask API URL
API_URL = "http://127.0.0.1:5000/expenses"

selected_expense_id = None

def fetch_expenses():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def display_expenses():
    for item in tree.get_children():
        tree.delete(item)
    expenses = fetch_expenses()
    for idx, expense in enumerate(expenses, start=1):
        tree.insert('', 'end', iid=expense['id'], values=(idx, expense['day'], expense['expenditure']))

def add_expense():
    global selected_expense_id
    day = entry_day.get()
    expenditure = entry_expenditure.get()
    if day and is_positive_number(expenditure):
        response = requests.post(API_URL, json={'day': day, 'expenditure': expenditure})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Expense added successfully")
            clear_fields()
            display_expenses()
        else:
            messagebox.showerror("Error", "Failed to add expense")
    else:
        messagebox.showerror("Error", "Please fill fields appropriately")

def update_expense():
    global selected_expense_id
    if selected_expense_id:
        day = entry_day.get()
        expenditure = entry_expenditure.get()
        if day and is_positive_number(expenditure):
            response = requests.put(f"{API_URL}/{selected_expense_id}", json={'day': day, 'expenditure': expenditure})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Expense updated successfully")
                clear_fields()
                display_expenses()
                selected_expense_id = None
            else:
                messagebox.showerror("Error", "Failed to update expense")
        else:
            messagebox.showerror("Error", "Please fill all fields")
    else:
        messagebox.showerror("Error", "Please select an expense to update")

def delete_expense():
    global selected_expense_id
    if selected_expense_id:
        response = requests.delete(f"{API_URL}/{selected_expense_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Expense deleted successfully")
            clear_fields()
            display_expenses()
            selected_expense_id = None
        else:
            messagebox.showerror("Error", "Failed to delete expense")
    else:
        messagebox.showerror("Error", "Please select an expense to delete")

def clear_fields():
    global selected_expense_id
    entry_day.delete(0, tk.END)
    entry_expenditure.delete(0, tk.END)
    selected_expense_id = None

def on_tree_select(event):
    global selected_expense_id
    selected_item = tree.selection()
    if selected_item:
        selected_expense_id = selected_item[0]
        selected_expense = tree.item(selected_item, 'values')
        entry_day.delete(0, tk.END)
        entry_day.insert(0, selected_expense[1])
        entry_expenditure.delete(0, tk.END)
        entry_expenditure.insert(0, selected_expense[2])

def is_positive_number(value):
    try:
        number = float(value)
        if number > 0:
            return True
        else:
            return False
    except ValueError:
        return False

# Create main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x400")
root.resizable(False,False)
root.configure(bg='peachpuff')

# Load custom icon
icon_path = 'C:\\Users\\asus\\Downloads\\money.png'  # Replace with the path to your icon file
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)  

# Create labels and entries
label_day = tk.Label(root, text="Day of Expense", fg="black", bg="peachpuff", font=("Helvetica", 12))
label_day.grid(row=0, column=0, padx=10, pady=10)
entry_day = tk.Entry(root, font=("Helvetica", 12))
entry_day.grid(row=0, column=1, padx=10, pady=10)

label_expenditure = tk.Label(root, text="Expenditure", fg="black", bg="peachpuff", font=("Helvetica", 12))
label_expenditure.grid(row=1, column=0, padx=10, pady=10)
entry_expenditure = tk.Entry(root, font=("Helvetica", 12))
entry_expenditure.grid(row=1, column=1, padx=10, pady=10)

# Create buttons with proper gaps
button_frame = tk.Frame(root, bg='peachpuff')
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

button_add = tk.Button(button_frame, text="Add", command=add_expense, font=("Helvetica", 12))
button_add.grid(row=0, column=0, padx=10)

button_update = tk.Button(button_frame, text="Update", command=update_expense, font=("Helvetica", 12))
button_update.grid(row=0, column=1, padx=10)

button_delete = tk.Button(button_frame, text="Delete", command=delete_expense, font=("Helvetica", 12))
button_delete.grid(row=0, column=2, padx=10)

button_clear = tk.Button(button_frame, text="Clear", command=clear_fields, font=("Helvetica", 12))
button_clear.grid(row=0, column=3, padx=10)

# Create Treeview for displaying expenses
columns = ('no', 'day', 'expenditure')
tree = ttk.Treeview(root, columns=columns, show='headings', style="Custom.Treeview")
tree.heading('no', text='No.')
tree.heading('day', text='Day of Expense')
tree.heading('expenditure', text='Expenditure')
tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Add scrollbar to Treeview
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=3, column=4, sticky='ns')

# Bind select event to Treeview
tree.bind('<<TreeviewSelect>>', on_tree_select)

# Style Treeview
style = ttk.Style()
style.configure("Custom.Treeview.Heading", font=("Helvetica", 12), background="grey")
style.configure("Custom.Treeview", background="white", foreground="black", fieldbackground="white")
style.map('Custom.Treeview', background=[('selected', 'skyblue')])

# Display expenses initially
display_expenses()

root.update()

# Centre Allocation

window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()
