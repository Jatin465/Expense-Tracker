from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/expense_tracker"
mongo = PyMongo(app)
expenses = mongo.db.expenses

def get_expenses():
    data = []
    for expense in expenses.find():
        data.append({
            'id': str(expense['_id']),
            'day': expense['day'],
            'expenditure': expense['expenditure']
        })
    return jsonify(data)

def add_expense(day, expenditure):
    expense_id = expenses.insert_one({'day': day, 'expenditure': expenditure}).inserted_id
    return {'id': str(expense_id)}

def update_expense(id, day, expenditure):
    expenses.update_one({'_id': ObjectId(id)}, {'$set': {'day': day, 'expenditure': expenditure}})
    return {'status': 'Expense updated'}

def delete_expense(id):
    expenses.delete_one({'_id': ObjectId(id)})
    return {'status': 'Expense deleted'}

@app.route('/expenses', methods=['GET'])
def get_expenses_route():
    return get_expenses()

@app.route('/expenses', methods=['POST'])
def add_expense_route():
    day = request.json['day']
    expenditure = request.json['expenditure']
    return jsonify(add_expense(day, expenditure))

@app.route('/expenses/<id>', methods=['PUT'])
def update_expense_route(id):
    day = request.json['day']
    expenditure = request.json['expenditure']
    return jsonify(update_expense(id, day, expenditure))

@app.route('/expenses/<id>', methods=['DELETE'])
def delete_expense_route(id):
    return jsonify(delete_expense(id))
