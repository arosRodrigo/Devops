from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Notas #base

collection = db.cupomFiscal #coleção

#mydict = { "name": "Anderson", "address": "Highway 37", "telefone": ["96394-6929","2507-6244"] } # documento

#x = collection.insert_one(mydict)
x = collection.find_one()


print(x)