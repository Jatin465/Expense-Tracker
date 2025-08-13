from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Crud']
collection = db['Operations']

# Create
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201

# Read
@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    try:
        item = collection.find_one({'_id': ObjectId(id)})
        if item:
            item['_id'] = str(item['_id'])
            return jsonify(item), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items', methods=['GET'])
def get_all_items():
    items = []
    for item in collection.find():
        item['_id'] = str(item['_id'])
        items.append(item)
    return jsonify(items), 200

# Update
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    data = request.json
    try:
        result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.matched_count:
            return jsonify({"message": "Item updated successfully"}), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Item deleted successfully"}), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

