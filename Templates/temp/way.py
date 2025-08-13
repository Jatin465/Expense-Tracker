# import pymongo

# myclient = pymongo.MongoClient('mongodb://localhost:27017/')

# mydb = myclient['simple']

# mycol = mydb["customers"]

# mycol.insert_one({"Name":"Rahul"})


# print(myclient.list_database_names())

# print(mydb.list_collection_names())


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["simple"]
mycol = mydb["customers"]

mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
]

x = mycol.insert_many(mylist)
print(x.inserted_ids)
# Read

y = mycol.find_one()

print(y)


myquery = { "address": "Mountain 21" }

mycol.delete_one(myquery)
for z in mycol.find():
  print(z)

# Update

myquery = { "address": "Valley 345" }
newvalues = { "$set": { "address": "Canyon 123" } }

mycol.update_one(myquery, newvalues)

for z in mycol.find():
  print(z)
  