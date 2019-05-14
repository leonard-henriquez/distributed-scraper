from hashlib import sha1
from datetime import datetime
from pymongo import MongoClient

from .settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

connection = MongoClient(MONGO_URI)
db = connection[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

def upload_article(article):
  url = article['url']
  article['timestamp_download'] = datetime.now().timestamp()
  article['_id'] = sha1(url.encode()).hexdigest()

  try:
    collection.insert_one(article)
  except:
    print("already in database")
