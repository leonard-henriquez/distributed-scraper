import time
from os import environ
from time import sleep
from hashlib import sha1
from datetime import datetime
from random import random
from pymongo import MongoClient
from .worker import app
from .medium_scraper import get_articles_url, get_article

client = MongoClient('mongodb://mongo:27017/articles')
db = client.articles
collection = db.medium

@app.task
def add_download(url):
  # Download & parse
  article = get_article(url)

  # Store
  article['timestamp'] = datetime.now().timestamp()
  article['_id'] = sha1(url.encode()).hexdigest()

  try:
    collection.insert_one(article)
  except:
    print("already in database")

  return True

@app.task
def add_source(tag, str_date):
  urls = get_articles_url(tag, str_date)

  for url in urls:
    print("Added {url} to download list".format(url=url))
    add_download.delay(url)

  return True
