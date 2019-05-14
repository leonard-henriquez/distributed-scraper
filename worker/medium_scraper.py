import re
from unicodedata import normalize
from datetime import datetime
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
      url = url.lower()
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


###############################


def string_sanitizer(string):
  string = normalize('NFKD', string)
  string = string.encode('ascii', 'ignore').decode()
  return string

def short_number_sanitizer(string):
  string = string_sanitizer(string)
  if len(string) == 0:
    value = 0
  elif string[-1] == 'K':
    value = int(float(string[0:-1]) * 1000)
  else:
    value = int(string)
  return value

def get_article(url):
  session = get_session()
  response = session.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')

  article = {}
  article['url'] = string_sanitizer(url).lower()

  title = soup.find('title').get_text()
  article['title'] = title

  try:
    lang = soup.find('article', {"lang": True}).get('lang')
    article['lang'] = string_sanitizer(lang).lower()
  except:
    pass

  try:
    ts = soup.find('time').get('datetime')
    ts = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    article['timestamp_published'] = ts.timestamp()
  except:
    pass

  author = soup.find('meta', {"name": "author"}).get('content')
  article['author'] = author

  author_link = soup.find('link', {"rel": "author"}).get('href')
  article['author_link'] = string_sanitizer(author_link).lower()

  try:
    author_site = soup.find('meta', {"property": "og:site_name"}).get('content')
    article['author_site'] = string_sanitizer(author_site).lower()
  except:
    pass

  try:
    tags_1 = soup.findAll('a', attrs={"data-action-source": "post", "href": re.compile("https?://medium.com/tag/")})
    tags_2 = soup.findAll('a', attrs={"data-action-source": "post", "data-collection-slug": True})
    tags = tags_1 + tags_2
    article['tags'] = [string_sanitizer(x.get_text().lower()) for x in tags]
  except:
    pass

  try:
    claps = soup.find('button', {"data-action":"show-recommends"}).get_text().split()[0]
    article['claps'] = short_number_sanitizer(claps)
  except:
    article['claps'] = 0

  try:
    reading_time = int(soup.find('span', {"class":"readingTime"}).get('title').split()[0])
    article['reading_time'] = reading_time
  except:
    article['reading_time'] = 0

  paragraphs = soup.findAll('p')
  text = ''
  next_line = '\n'
  for paragraph in paragraphs:
      text += paragraph.get_text() + next_line
  article['text'] = text
  return article
