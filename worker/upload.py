from hashlib import sha1
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from .settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

try:
    connection = MongoClient(MONGO_URI)
    connection.server_info()
    db = connection[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]
except ServerSelectionTimeoutError as err:
    print(err)

def upload_article(article):
  url = article['url']
  id = sha1(url.encode()).hexdigest()
  article['_id'] = id
  article['timestamp_download'] = datetime.now().timestamp()

  collection.update_one({"_id": id}, {"$set": article}, True)
