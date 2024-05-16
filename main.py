from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from notifypy import Notify

import os

from bs4 import BeautifulSoup

from datetime import datetime

from pymongo import MongoClient

#connecting to mongodb database
client=MongoClient("mongodb://localhost:27017/")
db=client["amazon"]
collection=db["prizes"]

def get_data():
    options=Options()
    #options.add_argument("--headless")
    #options.add_argument("--proxy-server=gate.nodemaven.com:8080")

    user_agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"


    with open("products.txt") as f:
        products = f.readlines()

    driver = webdriver.Chrome(options=options)

    i=0
    for product in products:
        driver.get(product.strip())
        import time
        time.sleep(25)
        i=i+1
        page_source = driver.page_source
        with open(f"data/product{i}.html", "w", encoding="utf-8") as f:
            f.write(page_source)


def extract_data():
    files = os.listdir("data")
    for file in files:
        print(file)
        with open(f"data/{file}", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')

            #extracting title from html
            title = soup.title.getText().split(":")[0]
            time=datetime.now()
            print(title)
            print(time)


            #extracting price from html
            price = soup.find(class_="a-price-whole")
            priceInt = price.getText().replace(",", "").replace(".", "")
            print(priceInt)  # removing all semicolan and dots from the prizes
            
            #extracting AISN Serial from html
            table = soup.find(id="productDetails_detailBullets_sections1")
            asin=""
            if table:
                asin = table.find(class_="prodDetAttrValue").getText().strip()
                if asin:
                    print(asin)
                else:
                    print("ASIN not found")
            else:
                print("Table not found")
            
            #writing data in finaldata.txt in append mode because in write mode it will overwrite the previous data

            #with open("finaldata.txt","a") as f:
                #f.write(f"{asin}~~{priceInt}~~{title}~~{time}\n")

                
            
            #inserting data in mongodb database
            collection.insert_one({"asin":asin,"priceInt":priceInt,"title":title,"time":time})

    pass


if __name__ == "__main__":
   notification=Notify()
   notification.title="Data Extraction from Amazon"
   notification.message="Web Scrapping Amazon!"
   notification.send()



get_data()
extract_data()





        





