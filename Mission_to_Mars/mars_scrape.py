#Import Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from flask_pymongo import PyMongo



mars = { }
image_links = []
image_titles = []

#def init_browser():
#    # @NOTE: Replace the path with your actual path to the chromedriver
#    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#    return Browser("chrome", **executable_path, headless=False)


def scrape():
    #Article title and paragraph
    url="https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    article_ = soup.find('div', class_="content_title")
    article = article_.find('a').text
    paragraph = soup.find('div', class_="rollover_description_inner").get_text()
    mars.update({"mars_article": article })
    mars.update({"mars_paragraph": paragraph })
    #Mars picture and picture title
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    #Find part of the link url
    image_mars= soup.find('footer').find('a').get("data-fancybox-href")
    #Create image link
    picture= f"{base_url}{image_mars}"
    #Find image title
    picture_title=soup.find("h1", class_ ='media_feature_title').text
    mars.update({"mars_picture": picture})
    mars.update({"mars_picture_title": picture_title })
    #Mars images
    #Loop through pages
    for x in range (4):
     #Use Splinter to visit the given page
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)
        url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)

        html = browser.html
        soup = bs(html, 'html.parser')
        base_url = "https://astrogeology.usgs.gov"
    #Find link to next page
        link_ = soup.find('div', class_="collapsible results").find_all('div', class_="item")
        link= link_[x].find("a", class_= "itemLink product-item").get("href")
    #Create the new link
        target_link= f"{base_url}{link}"
    #Visit the target link
        browser.visit(target_link)
#        response4 = requests.get(target_link)
#    html = browser.html
        soup = bs(html, 'html.parser')
    #Find title
        image_title=soup.find('title').get_text()
        image_titles.append(image_title)
        #Find image
        image_link= soup.find('img', class_="thumb").get('src')
        image_link_= f"{base_url}{image_link}"
        image_links.append(image_link_)
        mars.update({"mars_image_links": image_links })
        mars.update({"mars_image_titles": image_titles })
    return mars
