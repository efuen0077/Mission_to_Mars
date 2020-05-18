
#import Splinter and BeautifuylSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

#Set executable path and initialize the chrome
#browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

#by adding "browser" we are telling Python that we'll be using the
#"browser". variable defined above
def mars_news(browser):
    
    
    #assign url and instruct browser to visit
    #visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    #telling the browser to wait a second bc the page
    #is image heavy
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    #set up HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    #parent element : holds all other elements
    #ul = tag and item_list = class
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    slide_elem.find("div", class_='content_title')

    

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title


    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    news_p
    
            # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as #'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None
  
    return news_title, news_p

def featured_image(browser):
    #we must find a specific image.
# Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Find and click the full image button


    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')


    # Find the relative image url
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    #img_url_rel


    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    try:
   # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
    
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def scrape_all():
    # Initiate headless driver for deployment
    
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
       # Run all scraping functions and store results in dictionary

    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now()
    }

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

#pandas-friendly representation of the HTML table in the 
#webpage
#df = pd.read_html('http://space-facts.com/mars/')[0]
#df.columns=['description', 'value']
#df.set_index('description', inplace=True)
#df

#how to we add the table to our app?
#df.to_html

#we can end the automated browsing session.
#This is an important line to add to our web app also.
#Without it, the automated browser won’t know to shut
#down—it will continue to listen for instructions and use
#the computer’s resources (it may put a strain on memory or a 
#laptop’s battery if left on). We really only want the automated
#browser to remain active while we’re scraping data.

browser.quit()


# In[ ]:




