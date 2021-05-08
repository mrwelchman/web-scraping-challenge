# dependancies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
	executable_path = {'executable_path': ChromeDriverManager().install()}
	return Browser('chrome', **executable_path, headless=False)

def scrape():
	browser = init_browser()
	mars_feed = {}

	# nasa mars news
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	time.sleep(0.3)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	mars_feed['headline'] = soup.find('div', class_='bottom_gradient').find_all('h3')[0].text.strip()
	mars_feed['summary'] = soup.find('div', class_='article_teaser_body').get_text()

	# jpl featured image
	url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
	browser.visit(url)
	time.sleep(0.3)

	browser.find_by_id('filter_Mars').click()
	browser.find_by_css('.BaseImage').first.click()

	time.sleep(0.3)

	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	mars_feed['image_url'] = soup.find('img', class_='BaseImage')['data-src']

	# mars facts
	url = 'https://space-facts.com/mars/'
	tables = pd.read_html(url)
	mars_facts = tables[0]
	mars_facts.columns = ['Description', 'Mars']
	mars_facts.set_index('Description', inplace=True)
	mars_feed['mars_facts_web'] = mars_facts.to_html(classes='table table-striped')

	# hemispheres
	hemispheres = []
	url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

	
	for x in range(0,4):
		browser.visit(url)
		hems_dict = {}
		browser.find_by_css('h3')[x].click()
		time.sleep(0.3)
												
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')

		hems_dict['title']=soup.find('h2', class_='title').get_text()
		hems_dict['img_url']=soup.li.find('a')['href']

		hemispheres.append(hems_dict)

	browser.quit()
	mars_feed['hemispheres'] = hemispheres
	return mars_feed