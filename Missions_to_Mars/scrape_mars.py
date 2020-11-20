# Dependencies
from bs4 import BeautifulSoup
import html
from splinter import Browser
from urllib.parse import urljoin
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    mars_scrape = []

    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    for x in soup.find_all('div', class_='content_title'):
        if x.find('a') != None:
            news_headline = x.find('a')
            break
    news_headline = news_headline.text

    news_p = soup.find('div', class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = urljoin(url, featured_image_url)

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)

    table_html = tables[0].to_html()
    table_html = table_html.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    x = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', class_='itemLink product-item')
    links
    for link in links:
        link = urljoin(url, link['href'])
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_hemi = soup.find('img', class_='wide-image')['src']
        img_url = urljoin(url, mars_hemi)
        img_title = soup.find('h2', class_='title').text
        img_title = img_title.replace(' Enhanced', '')

        new_dict = {
            'title': img_title,
            'url': img_url
        }
        x.append(new_dict)

    mars_scrape = {
        'news_headline': news_headline,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'table_html': table_html,
        'list_dict': x
    }

    browser.quit()

    return mars_scrape
