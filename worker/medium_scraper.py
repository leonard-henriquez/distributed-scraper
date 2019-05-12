from selenium import webdriver
from bs4 import BeautifulSoup

def open_chrome():
  """
  OPENS A CHROME DRIVER
  """
  options = webdriver.chrome.options.Options()
  options.binary_location = '/usr/bin/chromium-browser'
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=options)
  driver.implicitly_wait(30)
  return driver


def find_post_cards(soup):
  """
  PULLS EACH CARD FROM THE FEED. EACH CARD IS A STORY OR COMMENT
  """
  cards = soup.find_all(
    "div", class_="streamItem streamItem--postPreview js-streamItem")
  return cards


def get_urls_from_cards(cards):
  """
  PARSE ARTICLE URLS FROM ALL CARDS
  """
  urls = []
  for card in cards:
    link = card.find("a", class_="")
    if link is not None:
      url = link['href']
      url = url[:url.find('?')]
      urls.append(url)
  return urls

def get_articles_url(tag, str_date):
  """
  GETS ARTICLE URLS FROM TAG AND DATE
  """
  # Create url from date
  base_url = "https://medium.com/tag/" + tag + "/archive/"
  url = base_url + str_date

  # Download list
  chrome_driver = open_chrome()
  chrome_driver.get(url)
  soup = BeautifulSoup(chrome_driver.page_source, features='lxml')

  # Parse list
  cards = find_post_cards(soup)
  urls = get_urls_from_cards(cards)

  # Add list elements to queue
  return urls
