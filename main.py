from bs4 import BeautifulSoup
import requests
import pandas as pd 
import re
import time
import sqlite3
import json

URL = "https://www.amazon.com/s?i=garden&srs=10158976011&bbn=10158976011&dc&qid=1723939935&ref=sr_nr_i_1"

#header for request
HEADERS = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept-Language' : 'en-US, en;q=0.5',
            'referer': 'https://google.com',})
#the request itself
webpage = requests.get(URL, headers=HEADERS)
#soup object contains all data
print(webpage)
searchdata = BeautifulSoup(webpage.content, "html.parser")

#this is my SQL database
def setup_database():
    conn = sqlite3.connect('amazon_products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            categories TEXT,
            image TEXT,
            link TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_product(name, price, categories, image, link):
    conn = sqlite3.connect('amazon_products.db')
    cursor = conn.cursor()
    categories_json = json.dumps(categories)
    cursor.execute('''
        INSERT INTO products (name, price, categories, image, link)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, price, categories_json, image, link))
    conn.commit()
    conn.close()

def fetch_all_products():
    conn = sqlite3.connect('amazon_products.db')  # Connect to your database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()  # Fetch everying in db
    conn.close()
    products_list = []
    for product in products:
        # Deserialize the JSON string back into a Python list
        categories_list = json.loads(product[3])
        products_list.append({
            'id': product[0],
            'name': product[1],
            'price': product[2],
            'categories': categories_list,
            'image': product[4],
            'link': product[5]
        })
    return products

# Fetch the first row and print it



def cuturl(url):
    return re.split(r'ref=[^&]*', url)[0]


def get_name(data):
    # Outer Tag Object
    name = data.find("span", attrs={"id":'productTitle'}).text.strip()
    #title_value = title.text
    #title_string = title_value.strip()
    return name

#gets the price and savings percentage
def get_price(data):
    try:
        price= data.find("span", attrs={'class':'aok-offscreen'}).text
    except AttributeError:
        try:
            price= data.find("span", attrs={'class':'a-offscreen'}).text
    
        except: price=""
    return price


#gets the directories main tag
def get_categories(data):
    try:
        directories = data.find("ul", attrs={'class':'a-unordered-list a-horizontal a-size-small'}).find_all("span", attrs={'class':'a-list-item'})
    #gets all categories, puts them into one array called directory_texts
        directory_texts = []
        for directory in directories:
            link_tag = directory.find("a", attrs={'class': 'a-link-normal a-color-tertiary'})
            if link_tag:
                directory_texts.append(link_tag.text.strip())
    except AttributeError:
        directories = data.find("span", attrs={'class':'cat-link'})
    #gets all categories, puts them into one array called directory_texts
        directory_texts = []
        directory_texts.append(directories)
    #print(directory_texts)
    return directory_texts


#gets the product image
def get_image(data):
    bigimage = data.find("div", attrs={'class':'imgTagWrapper'}).find('img')
    imagelink = bigimage['src']
    #print(imagelink)
    return imagelink

#find links as a list of tag objects
Links = searchdata.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
#link= Links[2].get('href')
#product_list = "https://amazon.com" + link
#print(product_list)
links_list = []
for link in Links:
    link_long_version=(link.get('href'))
    link_short = cuturl(link_long_version)
    links_list.append(link_short)


#now links_list has ALL the links to the products
#d = {"name":[], "price":[], "categories":[], "image":[]}
#now for the product page
#productURL=product_list
#productpage = requests.get(productURL, headers=HEADERS)
#productdata = BeautifulSoup(productpage.content, "html.parser")

setup_database()
for link in links_list:
    if link.startswith("https:"):
        productpage = requests.get(link, headers=HEADERS)
        procut_link = link
    else:
        productpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        product_link = ("https://www.amazon.com" + link)
    time.sleep(1)
    newdata = BeautifulSoup(productpage.content, "html.parser")

    # Function calls to get all necessary product information
    name = get_name(newdata)                               
    price = get_price(newdata)
    categories = get_categories(newdata)
    image = get_image(newdata)

    insert_product(name, price, categories, image, product_link)


products = fetch_all_products()
for product in products:
    print(product)

"""
#product page is the page itself, we are requesting it.
link=links_list[5]
if link.startswith("https:"):
    productpage = requests.get(link, headers=HEADERS)
else:
    productpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
#newdata is the contSent on the product page
newdata = BeautifulSoup(productpage.content, "html.parser")
print("https://www.amazon.com" + links_list[5])
print(get_name(newdata))
print(get_price(newdata))
print(get_image(newdata))
print(get_categories(newdata))
"""
#this is the temporary database
#database = open("myfile.txt", "a")
#database.write(str(d))
#database.write(str(links_list))

'''
#query all entries
def fetch_all_products():
    conn = sqlite3.connect('amazon_products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

# Fetch and print all products
products = fetch_all_products()
for product in products:
    print(product)

'''