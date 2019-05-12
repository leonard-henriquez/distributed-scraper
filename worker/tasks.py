import time
from time import sleep
from random import random
from .worker import app
from .medium_scraper import get_articles_url

@app.task
def task_wait_3s():
  print("long time task begin")
  sleep(3)
  print("long time task finished")
  return random()

@app.task
def add_download(url):
  # Download
  # Parse
  # Store
  return True

@app.task
def add_source(tag, str_date):
  urls = get_articles_url(tag, str_date)
  for url in urls:
    add_download.delay(url)
    print("Added {url} to download list".format(url=url))
  return True
