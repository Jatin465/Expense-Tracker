from flask import Flask, request, jsonify
from bson import ObjectId
from database import ExpenseDB

app = Flask(__name__)
db = ExpenseDB()

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = db.get_expenses()
    for expense in expenses:
        expense['_id'] = str(expense['_id'])
    return jsonify(expenses)

@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = request.json
    result = db.add_expense(expense)
    return jsonify({"_id": str(result.inserted_id)}), 201

@app.route('/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    update = request.json
    result = db.update_expense(ObjectId(expense_id), update)
    return jsonify({"modified_count": result.modified_count})

@app.route('/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    result = db.delete_expense(ObjectId(expense_id))
    return jsonify({"deleted_count": result.deleted_count})

if __name__ == '__main__':
    app.run(debug=True)
