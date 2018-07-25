
# coding: utf-8

# # Step 1 - Scraping

# In[2]:


from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests


# In[3]:

def scrape():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    time.sleep(1)

    

# # NASA Mars News

# In[4]:


# Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    print(news_title)
    print(news_p)

    

# # JPL Mars Space Images - Featured Image

# In[5]:


# Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# Make sure to find the image url to the full size `.jpg` image.
# Make sure to save a complete url string for this image.

    url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

# Scrape the browser into soup and use soup to find the image of mars
# Save the image url to a variable called `img_url`
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    #image = soup.find("article", class_="carousel_item")["style"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

# Use the requests library to download and save the image from the `img_url` above
    import shutil
    response = requests.get(img_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    
# Display the image with IPython.display
    from IPython.display import Image
    Image(url='img.jpg')    


# # Mars Weather

# In[6]:


# visit the mars weather report twitter and scrape the latest tweet
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    mars_weather_soup = BeautifulSoup(html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    print(mars_weather)


# # ### Mars Facts

# In[7]:


# visit space facts and scrape the mars facts table
    request_mars_space_facts = requests.get("https://space-facts.com/mars/")

    mars_space_table_read = pd.read_html(request_mars_space_facts.text)

    mars_space_table_read


# In[8]:


    df = mars_space_table_read[0]
    df.set_index(0, inplace=True)

    mars_data_df = df
    mars_data_df


# In[9]:


    mars_data_html = mars_data_df.to_html()
    mars_data_html

    mars_data_html.replace('\n', '')


# In[10]:


# save to HTML table
    mars_data_df.to_html('mars_table.html')


# # Mars Hemispheres

# In[14]:


# scrape images of Mars' hemispheres from the USGS site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_dicts = []

    for i in range(1,9,2):
        mars_dict = {}
        hemi_dict = {}
    
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        name_links = soup.find_all('a', class_='product-item')
        title = name_links[i].text.strip('Enhanced')
    
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        browser.find_link_by_text('Sample').first.click()
        browser.windows.current = browser.windows[-1]
        img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
    
        img_soup = BeautifulSoup(img_html, 'html.parser')
        img_url = img_soup.find('img')['src']

        hemi_dict['title'] = title.strip()

        hemi_dict['img_url'] = img_url

        mars_dicts.append({"Title": title, "Image_Url": img_url})


        #print(mars_dicts)
        print(hemi_dict)

    browser.quit()

    return to_flask_dict


mars_data = {}

mars_data = {"News Title": news_title, "News Paragraph": news_p, "Featured Image": img_url, "Mars Weather": mars_weather, "Mars Data": mars_data_html, "Mars Images": hemi_dict}

