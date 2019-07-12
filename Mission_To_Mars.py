
# Import dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pprint

def browser_init():
#  Chromedriver setup
    executable_path = {'executable_path': 'C:/ChromeDriver/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Begin scrape function
def scrape():
    # Call browser
    browser = browser_init()
    # Scraped url
    url = 'https://mars.nasa.gov/news/'

    # Retrieve data from request
    response = requests.get(url)

    # Create BeautifulSoup object
    soup = bs(response.text, 'html.parser')

    # Return article title
    news_title = soup.title.get_text()

    # Return article body
    news_bod = soup.p.get_text()

    # Scraping NASA Site for Mars image
    # Visit image url
    image_url = ('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    browser.visit(image_url)

    # Save featured image url
    featured_image_url = (
        'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16729_hires.jpg')

    # Scraping MarsWxReport Twitter page
    # Visit Twitter
    twt_url = ('https://twitter.com/marswxreport?lang=en')
    browser.visit(twt_url)

    # Retrieve data from request
    response_twt = requests.get(twt_url)

    # Create BeautifulSoup object
    soup_twt = bs(response_twt.text, 'html.parser')

    # Retrieve latest tweet, class found by manual searching in BS object
    latest_tweet = soup_twt.find(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    # Pull text from latest tweet, print
    mars_weather = latest_tweet.get_text()

    # Scraping Space Facts site for Mars facts with Pandas
    # Scrape facts site with pandas
    facts_url = ('https://space-facts.com/mars/')
    facts_table = pd.read_html(facts_url)

    # # Set up facts dataframe
    facts_df = facts_table[0]
    facts_df.columns = ['Description', 'Value Mars', 'Value Earth']
    facts_df.set_index('Description', inplace=True)
    facts_dict = facts_df.to_dict()

    # # Push pandas df to html table
    facts_df.to_html('facts_table.html')

    # Scraping Mars Hemispheres Site
    # Visit cerberus page
    cerberus_url = (
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')
    browser.visit(cerberus_url)

    # Retrieve data from request
    response_cerberus = requests.get(cerberus_url)

    # Create BeautifulSoup object
    soup_cerberus = bs(response_cerberus.text, 'html.parser')

    # Retrieve Title
    cerberus_title = soup_cerberus.find("h2", class_='title').get_text()
    # cerberus_title

    # Visit schiaparelli page
    schia_url = (
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')
    browser.visit(schia_url)

    # Retrieve data from request
    response_schia = requests.get(schia_url)

    # Create BeautifulSoup object
    soup_schia = bs(response_schia.text, 'html.parser')

    # Retrieve Title
    schia_title = soup_schia.find("h2", class_='title').get_text()
    # schia_title

    # Visit syrtis page
    syrtis_url = (
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')
    browser.visit(syrtis_url)

    # Retrieve data from request
    response_syrtis = requests.get(syrtis_url)

    # Create BeautifulSoup object
    soup_syrtis = bs(response_syrtis.text, 'html.parser')

    # Retrieve Title
    syrtis_title = soup_syrtis.find("h2", class_='title').get_text()
    # syrtis_title

    # Visit valles page
    valles_url = (
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')
    browser.visit(valles_url)

    # Retrieve data from request
    response_valles = requests.get(valles_url)

    # Create BeautifulSoup object
    soup_valles = bs(response_valles.text, 'html.parser')

    # Retrieve Title
    valles_title = soup_valles.find("h2", class_='title').get_text()
    # valles_title

    # Define hemisphere image urls
    cerberus_img = (
        'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg')
    schia_img = (
        'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg')
    syrtis_img = (
        'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg')
    valles_img = (
        'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg')

    # Store data in dictionary
    mars_data = {
        "Article Title" : news_title,
        "Article Body" : news_bod,
        "Featured Image" : featured_image_url,
        "Mars Weather" : mars_weather,
        "Cerberus" : cerberus_title,
        "Cerberus Image" : cerberus_img,
        "Schiaparelli" : schia_title,
        "Schiaparelli Image": schia_img,
        "Syrtis" : syrtis_title,
        "Syrtis Image" : syrtis_img,
        "Valles" : valles_title,
        "Valles Image" : valles_img
    }

    def Merge(dict1, dict2): 
        res = {**dict1, **dict2} 
        return res
    merged_data = Merge(facts_dict, mars_data)

    # Close the browser after scraping
    browser.quit()

    print('Scrape Complete! Here is your data!')
    pprint.pprint(merged_data)
    return merged_data

mars_scrape = scrape()

# Begin MongoDB section
import pymongo

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.mars_database
collection = db.stats

db.collection.insert_one(mars_scrape)