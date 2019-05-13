import requests
from fake_useragent import UserAgent

ua = UserAgent()
ua.update()

def get_session():
  """
    Creates a sessions using rproxy and fake user agent
  """
  session = requests.session()
  session.proxies = {
    'http': 'rproxy:5566',
    'https': 'rproxy:5566'
    }
  session.headers = get_headers()
  return session


def get_headers():
  """
    Creates headers with random user agent
  """
  headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": ua.random
  }
  return headers
