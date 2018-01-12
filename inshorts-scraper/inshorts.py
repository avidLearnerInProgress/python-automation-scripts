import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

print("Scraping the news ....")

my_url = 'https://www.inshorts.com/en/read'
uClient = uReq(my_url)

page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,"html.parser")


containers = page_soup.findAll("div",{"class":"news-card-title news-right-box"})


i = 1
for container in containers:
    print(i ,"." , container.span.text) 
    i+= 1
    time.sleep(2)
print("\n")