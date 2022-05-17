
# Import Splinter and BeautifulSoup
from turtle import title
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    hemispheres_image_urls = hemisphere_data(browser)

    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(), 
          "hemisphere_image_urls": hemisphere_data(browser)
    }
    
   # Stop webdriver and return data
    browser.quit()
    return data


#insert function, add argument to function ('browser')
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert broswer html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p



# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    
    # Use base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())



def hemisphere_data(browser):    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for hemisphere_url in range(4):
        browser.find_by_tag('h3').links.find_by_partial_text('Enhanced')[hemisphere_url].click()
        
        #parse with soup
        html = browser.html
        image_soup = soup(html, 'html.parser')
        
        # identify hemisphere URL and Title
        title = image_soup.find('h2').get_text()
        image_url = image_soup.find('li').find('a').get('href')
        
        # create empy dictionary inside for loop (#3)
        hemispheres = {}

        # add image url and title to dict
        hemispheres['title'] = title
        hemispheres['img_url']= f'https://marshemispheres.com/{image_url}'
        hemisphere_image_urls.append(hemispheres)
        
        # go back to main homepage
        browser.back()
    
        return hemisphere_image_urls

