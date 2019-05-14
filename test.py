from pymongo import MongoClient
from datetime import datetime
from os import environ

try:
  mongo_uri = environ["MONGO_URI"]
  connection = MongoClient(mongo_uri)
except:
  print("Could not connect to MongoDB")
  exit()

db = connection.articles
collection = db.medium

results = collection.count_documents({})
print("Number of results:", results)

if results != 0:
  last = collection.find().sort("timestamp_download", -1).limit(1)
  ts = datetime.fromtimestamp(last[0]["timestamp_download"])
  print("Last input", ts.strftime("%d/%m/%y %H:%M"))
  print("Last input", last[0])
