import os
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def open_chrome():
	"""
	OPENS A CHROME DRIVER
	"""
	options = webdriver.chrome.options.Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
	driver.implicitly_wait(30)
	return driver


def find_post_cards(soup):
	"""
	PULLS EACH CARD FROM THE FEED. EACH CARD IS A STORY OR COMMENT
	"""
	cards = soup.find_all("div", class_="streamItem streamItem--postPreview js-streamItem")
	return cards


def get_urls_from_cards(cards):
	"""
	GETS ARTICLE URLS FROM ALL CARDS
	"""
	urls = []
	for card in cards:
		link = card.find("a", class_="")
		if link is not None:
			url = link['href']
			url = url[:url.find('?')]
			urls.append(url)
	return urls


def scrape_tag(tag, begin_date, end_date=None):
	# BUILDS THE BASE URL FROM GIVEN TAG TO ITERATE ON
	base_url = "https://medium.com/tag/" + tag + "/archive/"

	# MEDIUM DENIES ANY COMMANDLINE REQUESTS, NEED BROWSER
	chrome_driver = open_chrome()

	# START ITERATION OVER DATES
	end_date = end_date or datetime.now()
	current_date = end_date
	while(current_date >= begin_date):
		# BUILD URL FROM CURRENT_DATE
		url = base_url + current_date.strftime("%Y/%m/%d")

		# DOWNLOAD WEBPAGE
		chrome_driver.get(url)

		# PARSE WEB RESPONSE
		soup = BeautifulSoup(chrome_driver.page_source, features='lxml')

		# FIND ALL STORY CARDS, EACH IS AN ARTICLE
		cards = find_post_cards(soup)

		# FIND ALL URL
		urls = get_urls_from_cards(cards)
		print(current_date.strftime("%Y/%m/%d"))
		print(urls)

		# ADDS A DAY TO THE CURRENT DATE FOR NEXT URL CALL
		current_date = current_date - timedelta(days=1)

		# WAIT BEFORE NEXT REQUEST
		time.sleep(2)
	chrome_driver.close()

tags ='data-science'

for tag in tags.split(','):
	print("Starting to download tag ", tag)
	begin_date = datetime(2018, 1, 1)
	end_date = datetime(2018, 1, 10)
	scrape_tag(tag, begin_date)
	print("Done with tag ", tag)

print("done")
