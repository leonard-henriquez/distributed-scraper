from bs4 import BeautifulSoup
from .proxy import get_session

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
  session = get_session()
  response = session.get(url, timeout=5)
  print("-- STATUS " + str(response.status_code) + " -- " + url)
  if response.status_code == 200:
    # Parse list
    soup = BeautifulSoup(response.text, features='lxml')
    cards = find_post_cards(soup)
    urls = get_urls_from_cards(cards)
  else:
    print('Wrong response. Status code', response.status_code)
    return False

  # Add list elements to queue
  return urls
