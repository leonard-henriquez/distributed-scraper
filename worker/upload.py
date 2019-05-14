from hashlib import sha1
from datetime import datetime
from pymongo import MongoClient

from .settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

connection = MongoClient(MONGO_URI)
db = connection[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

def upload_article(article):
  url = article['url']
  id = sha1(url.encode()).hexdigest()
  article['_id'] = id
  article['timestamp_download'] = datetime.now().timestamp()

  collection.update_one({"_id": id}, {"$set": article}, True)
