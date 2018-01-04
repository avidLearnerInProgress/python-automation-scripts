#Techcrunch Scraper
from bs4 import BeautifulSoup
import urllib.request as req
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import numpy as np
import csv
from six.moves import cPickle as pickle
import numpy as np


def displayPickleData(path_pickle):
    x = []
    with open(path_pickle,'rb') as f:
        x = pickle.load(f,encoding='iso-8859-15')
    print(x)

def grabTechcrunch():
	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Firefox(firefox_options=options)
	print("Firefox Headless Browser Invoked")
	tc_df = pd.DataFrame(index = np.arange(0,), columns = ('Title','Summary','Link'))
	article_index = 0
	#Iterate through each page
	#Each page fetches approx 20 article links
	try:
		for page_num in range(1,5):
			url = 'https://techcrunch.com/page/'+str(page_num)
			driver.get(url)
			news_items = driver.find_elements_by_class_name('river-block')
			for news_item in news_items:
				post_title = news_item.find_element_by_class_name('post-title')
				post_url = news_item.get_attribute("data-permalink")
				try:
					data_summary = news_item.find_element_by_class_name("excerpt")
					data_entry = [post_title.text,data_summary.text,post_url]
				except Exception as e:
					non_obj = None
					data_entry = [post_title.text,non_obj,post_url]
				tc_df.loc[article_index]= data_entry
				print(data_entry)
				article_index += 1
		#driver.close()
		print("Driver Closed")
		tc_df.to_pickle('techcrunch.pkl')
		displayPickleData('techcrunch.pkl')

	except Exception as e:
		driver.close()
		print('Error!'+str(e))

def main():
	grabTechcrunch()
	#convert('techcrunch.pkl','techcrunch.csv')

if __name__ == '__main__':
	main()


'''todo
1. convert to csv properly
2. user input for number of pages
'''