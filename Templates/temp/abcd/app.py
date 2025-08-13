from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/expense_tracker"
mongo = PyMongo(app)
expenses = mongo.db.expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    data = []
    for expense in expenses.find():
        data.append({
            'id': str(expense['_id']),
            'day': expense['day'],
            'expenditure': expense['expenditure']
        })
    return jsonify(data)

@app.route('/expenses', methods=['POST'])
def add_expense():
    day = request.json['day']
    expenditure = request.json['expenditure']
    expense_id = expenses.insert_one({'day': day, 'expenditure': expenditure}).inserted_id
    return jsonify({'id': str(expense_id)})

@app.route('/expenses/<id>', methods=['PUT'])
def update_expense(id):
    day = request.json['day']
    expenditure = request.json['expenditure']
    expenses.update_one({'_id': ObjectId(id)}, {'$set': {'day': day, 'expenditure': expenditure}})
    return jsonify({'status': 'Expense updated'})

@app.route('/expenses/<id>', methods=['DELETE'])
def delete_expense(id):
    expenses.delete_one({'_id': ObjectId(id)})
    return jsonify({'status': 'Expense deleted'})

if __name__ == '__main__':
    app.run(debug=True)
