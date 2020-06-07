#!/usr/bin/env python
# coding: utf-8

# # Code to compare Price of product on two different E-commerce websites.
# 
# # Lazada Website

# In[393]:


# Important libraries
# for web scraping
from selenium import webdriver
from selenium.common.exceptions import *

# for data manipulation
import pandas as pd

# for visualization 
import matplotlib.pyplot as plt
import seaborn as sns


# In[394]:


# url of website to parse
url = 'https://www.lazada.com.my' 

# product to parse
search_item = 'Nescafe Gold refill 170g'


# In[395]:


# custom chrome options
options = webdriver.ChromeOptions()

# options.add_argument('--headless') 
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

# open the browser
driver = webdriver.Chrome()
driver.get(url)

# find the search bar
search_bar = driver.find_element_by_id('q')
search_bar.send_keys(search_item)
click_button = driver.find_element_by_xpath('//*[@id="topActionHeader"]/div/div[2]/div/div[2]/form/div/div[2]/button')
click_button.click()

# find the products titles and prices
item_titles = driver.find_elements_by_class_name('c16H9d')
item_prices = driver.find_elements_by_class_name('c13VH6')


# In[396]:


# empty lists
titles_list, prices_list = [], []

# loopover the previous list elements
for title in item_titles:
    titles_list.append(title.text)
for price in item_prices:
    prices_list.append(price.text)
    
# the values in the titles_list and prices_list
print(titles_list)
print(prices_list)


# In[397]:


# if items are also available on the next page we have to check for it
try:
    driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[6]/a').click()
except NoSuchElementException:
    driver.quit()


# In[398]:


# now analyze the data
df = pd.DataFrame(zip(titles_list, prices_list), columns = ['ItemName', 'Price'])
print(df)


# In[399]:


# check the info of DataFrame
df.info()


# In[400]:


# change the datatype of Price column from object to float
df['Price'] = df['Price'].str.replace('RM', '').astype(float)


# In[401]:


# drop the result items which contains x 2 in it
df = df[df['ItemName'].str.contains('x{23} | x 2') == False]
print(df)


# In[402]:


# look for the condition that result items contain 170g in it
df = df[df['ItemName'].str.contains('170g') == True]
print(df)


# In[403]:


# add a new column to dataframe
df['Platform'] = 'Lazada'
print(df)


# In[404]:


# sort the index values from 0 to number of values in dataframe
df.index = range(len(df.index))
print(df)


# In[405]:


# describe the numerical column vlaues in dataframe
df.describe()


# In[406]:


# plot the chart of price values 
sns.set()
_ = sns.boxplot(x = 'Platform', y = 'Price', data = df)
_ = plt.title('Comparison of Nescafe Gold Refill 170g prices between e-commerce platforms in Malaysia')
_ = plt.ylabel('Price (RM)')
_ = plt.xlabel('E-commerce Platform')

# show the plot
plt.show()


# # Shopee website scrape using an API

# In[407]:


# requests library for web scraping
import requests
import re


# In[408]:


# website url
Shopee_url = 'https:://www.shopee.com.my'

# product we want to search
key_word_search = 'Nescafe Gold refill 170g'

# headers to pass to website call
headers = {
 'User-Agent': 'Chrome',
 'Referer': '{}search?keyword={}'.format(Shopee_url, key_word_search)
}

# API to search our product
url = 'https://shopee.com.my/api/v2/search_items/?by=relevancy&keyword={}&limit=100&newest=0&order=desc&page_type=search'.format(key_word_search)

# now we do a shopee API request
r = requests.get(url, headers = headers).json()

# shopee scraping script
titles_list = []
prices_list = []
for item in r['items']:
    titles_list.append(item['name'])
    prices_list.append(item['price_min'])


# In[409]:


# create dataframe from the collected titles and price list
shopee = pd.DataFrame(zip(titles_list, prices_list), columns = ['ItemName', 'Price'])


# In[410]:


# add another column
shopee['Platform'] = 'Shopee'


# In[411]:


# update the price and remove items which are not of weight 170g
shopee['Price'] /= 100000
shopee = shopee[shopee['ItemName'].str.contains('170g') == True]

# also remove x2 items
shopee = shopee[shopee['ItemName'].str.contains('[2x\s]{3}|twin', flags=re.IGNORECASE,regex=True) == False]


# In[412]:


print(shopee)


# In[413]:


# update index values
shopee.index = range(len(shopee.index))
print(shopee)


# In[414]:


# concat both the dataframes
master_df = pd.concat([df, shopee])

# update the index of master dataframes
master_df.index = range(len(master_df.index))
master_df


# In[415]:


print(master_df.groupby(['Platform']).describe())


# In[416]:


# now do ploting
sns.set()
_ = sns.boxplot(x='Platform', y='Price',data=master_df)
_ = plt.title('Comparison of Nescafe Gold Refill 170g prices between e-commerce platforms in Malaysia')
_ = plt.ylabel('Price (RM)')
_ = plt.xlabel('E-commerce Platform')

# Show the plot
plt.show()


# #### This graph shows that Shopee website is a cheaper platform to buy the products with more number of items.
