from pymongo import MongoClient

class ExpenseDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="expense_tracker"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["expenses"]

    def add_expense(self, expense):
        return self.collection.insert_one(expense)

    def get_expenses(self):
        return list(self.collection.find())

    def update_expense(self, expense_id, update):
        return self.collection.update_one({"_id": expense_id}, {"$set": update})

    def delete_expense(self, expense_id):
        return self.collection.delete_one({"_id": expense_id})
