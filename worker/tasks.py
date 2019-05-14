from requests.exceptions import ProxyError, ReadTimeout
from datadog import statsd
from .worker import app
from .medium_scraper import get_articles_url, get_article
from .upload import upload_article

@app.task(bind=True, autoretry_for=(ProxyError, ReadTimeout,), retry_backoff=5)
def add_download(self, url):
  # Download & parse
  article = get_article(url)

  # Store
  upload_article(article)

  # Increment download
  statsd.increment('download.finished')

  return True

@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def add_source(self, tag, str_date):
  urls = get_articles_url(tag, str_date)

  for url in urls:
    # Add url to download queue
    print("Added {url} to download list".format(url=url))
    add_download.delay(url)

    # Increment download queued
    statsd.increment('download.queue')

  return True
