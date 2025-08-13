from app import app, get_expenses, add_expense, update_expense, delete_expense

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
