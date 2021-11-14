import time
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
from PIL import Image
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

ready= input("Press Enter to Start!")
categorie = input("Enter Animal:")
number_of_pagedowns = input("Number of Pagedowns:")
number_of_pagedowns = int(number_of_pagedowns)


Path(categorie).mkdir(parents=True, exist_ok=True)


get_cat = "https://unsplash.com/s/photos/",categorie
new_get_cat = ''.join(get_cat)


driver.get(new_get_cat)
time.sleep(2)

elem = driver.find_element_by_tag_name("body")


try:
    driver.find_element_by_xpath("//button[text()='Load more photos']").click()
except: pass

no_of_pagedowns = number_of_pagedowns

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1



html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]
name = 1

for url in urls:
    try:
        img_data = requests.get(url).content  
        im = Image.open(BytesIO(img_data))
        if im.size[0] <= 100:
            pass
        if im.size[1] <= 100:
            pass
        else:
            try:
                req = categorie,"/",categorie,"_",str(name),".jpg"
                new_req = ''.join(req)
                urllib.request.urlretrieve(url,new_req)
                name = name + 1
            except: pass
    except: pass
    
driver.close()
print("Done!")