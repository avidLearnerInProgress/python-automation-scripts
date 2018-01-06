from bs4 import BeautifulSoup
import urllib.request as req
import pandas as pd
from heapq import merge
import json
import csv
from csv import DictWriter
import json_to_csv
import os

def writeToCSV(input_file):
    #os.system("cmd.exe activate py27")
    os.system("python json_to_csv.py" + " _ " + input_file + " result.csv")

def writeToJSON(resources):
    with open('data.json', 'w') as outfile:
        json.dump(resources, outfile)
    writeToCSV('data.json')

#Fetch top 30 news from news.ycombinator.com
def hackernewsScrape():
    
    # total_posts
    #pages = (total_posts/30) + 1;
    '''page_num = 1
    article_num = 1
    '''
    page_num = 1
    url = 'https://news.ycombinator.com/news?p=' + str(page_num)
    response = req.urlopen(url)
    data = response.read()
    soup = BeautifulSoup(data, "html5lib")
    title_items = soup.find("table", {"class": "itemlist"}).find_all("tr", {"class": "athing"})
    subtext_items = soup.find("table", {"class": "itemlist"}).find_all("td", {"class": "subtext"})
    n = 1
    resources = []
    for title_item in title_items:
        subtext_item = subtext_items[n-1]
        resources.append({
            "host": title_item.find_all("td", {"class": "title"})[1].find("span", {"class": "sitestr"}).text,
            "link": title_item.find_all("td", {"class": "title"})[1].find("a").get("href"),
            "title": title_item.find_all("td", {"class": "title"})[1].find("a").text
        })
        n += 1
    print(resources)
    writeToJSON(resources)

def main():
    #number = int(input('Number of posts to scrape -> '))
    #hackernewsScrape(number)
    #writeToCSV()
    hackernewsScrape()

if __name__ == '__main__':
    main()
