# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os

def scrape():
    # Read static HTML file
    file = os.path.join('NewsNASAMarsExplorationProgram', 'News_NASA_Mars_Exploration_Program.html')
    with open(file) as f:
        html = f.read()

    # Initialize one dict to hold all scraped variables
    data = {}

    # Create soup object for static HTML page
    soup = bs(html, 'lxml')

    # Scrape the headline title and article teaser text
    # Add it to the dictionary
    title = soup.find('div', class_ = 'content_title')
    data['news_title'] = title.find('a').text
    news_text = soup.find('div', class_ = 'article_teaser_body').text
    news_text = news_text.replace('\n', '')
    data['news_text'] = news_text

    # Scrape the featured image from the JPL site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url)
    image_soup = bs(response.text, 'lxml')
    # Set a base image url to append the rest of the URL string
    base_image_url = 'https://www.jpl.nasa.gov'
    # Scrape the url string and append it to the base URL
    stem_image_url = image_soup.find('a', class_ = 'button fancybox')['data-fancybox-href']
    data['featured_image_url'] = base_image_url + stem_image_url

    # Scrape the Weather Tweet(s)
    tweets_url = 'https://twitter.com/marswxreport?lang=en'
    tweets_response = requests.get(tweets_url)
    tweet_soup = bs(tweets_response.text, 'lxml')
    data['mars_weather'] = tweet_soup.find('p', class_ = 'TweetTextSize').text

    # Use pandas to convert Space Facts table to html table
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    # This should be interesting
    fact_table = df.to_html()
    fact_table.replace('\n', '')
    data['facts_table'] = fact_table

    # Initialize a list for the image data and set a base URL like previously
    hemisphere_image_urls = []
    hem_base_url = 'https://astrogeology.usgs.gov'

    # Setup to scrape the USGS site
    hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hems_response = requests.get(hems_url)
    hems_soup = bs(hems_response.text, 'lxml')
    hspheres = hems_soup.find_all('div', class_ = 'item')

    # Get all the image titles and loop through their links to find the actual image source
    for hem in hspheres:
        hem_dict = {}
        hem_dict['title'] = hem.find('h3').text.replace(' Enhanced', '')
        img_url = hem_base_url + hem.find('a')['href']
        img_response = requests.get(img_url)
        img_soup = bs(img_response.text, 'lxml')
        hem_dict['img_url'] = img_soup.find('a', target = '_blank')['href']
        hemisphere_image_urls.append(hem_dict)

    data['hemisphere_image_urls'] = hemisphere_image_urls

    return data
    
