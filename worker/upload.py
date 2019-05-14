from hashlib import sha1
from datetime import datetime
from pymongo import MongoClient

from .settings import MONGO_URI

connection = MongoClient(MONGO_URI)
db = connection.articles
collection = db.medium

def upload_article(article):
  url = article['url']
  article['timestamp_download'] = datetime.now().timestamp()
  article['_id'] = sha1(url.encode()).hexdigest()

  try:
    collection.insert_one(article)
  except:
    print("already in database")
