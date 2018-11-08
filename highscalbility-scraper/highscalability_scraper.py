#Scraping imports
from bs4 import BeautifulSoup as BS
import requests as R

#Random imports
import lxml, time, csv
from collections import OrderedDict
import pandas as pd 

def mk_soup(base_url):
	response = R.get(base_url)
	soup = BS(response.content, 'html.parser')
	return soup

def logging(msg = None):
	if msg is None:
		print("Error!")
	else:
		print(msg)
	time.sleep(2)
	exit()

def file_write_dict(filenm, _dct):
	if filenm is None or _dct is None:
		logging("Insufficient parameters!")
	else:
		with open(filenm, 'w', encoding = 'utf-8') as t:
			for ele1, ele2 in _dct.items():
				t.write(str(ele1) + "-->" + str(ele2) + "\n")

def file_write(filenm, lst):
	if filenm is None or lst is None:
		logging("Insufficient parameters!")
	else:
		with open(filenm, 'w', encoding = 'utf-8') as t:
			for ele in lst:
				t.write("%s\n" % ele)

def parser(base_url, nano_url):
	blog_urls = []
	blog_names = []
	pg_soup = mk_soup(base_url)
	class_ls = ["journal-archive-set", "h3subtitle"]
	dated_divs = pg_soup.find_all('div', class_ls)
	dated_divs = dated_divs[4] #Extract month wise blogs.. Wasted 10 min thinking how to do it.. later just played with it as its a list :p
	for date in dated_divs.find_all('a'):
		blog_urls.append(date.get('href'))
		blog_names.append(date.text)
	blog_urls_rev = blog_urls[:-1]
	blog_names_rev = blog_names[:-1]
	#nu_pairs = dict(zip(blog_names_rev, blog_urls_rev)) #This fcuk doesn't work as I am on Python 3.5 and dictionaries are unordered in this v.. Wish I used 3.6 somehow :(
	nu_pairs = OrderedDict(zip(blog_names_rev, blog_urls_rev)) #Had to resort to ordereddict.. Why did you take so much time in making dicts ordered @RaymondHettinger :|
	
	_urls = []
	for k,v in nu_pairs.items():
		complete_url = str(nano_url + v)
		_urls.append(complete_url)
	return _urls

def inner_sp_for_articles(month_sp = None):
	#print(month_sp)
	if month_sp is None:
		print("Invalid month..")
		time.sleep(2)
		exit()
	else:
		for articles in month_sp.find_all('h2', class_='title'):
				for article in articles.find_all('a'):
					ele_text = article.text
					ele_url = article['href']
					return ele_text, ele_url

def parse_each_url(base_url = None, nano_url = None):
	
	all_ele_text, all_ele_url = [], []
	if base_url is None or nano_url is None:
		logging("Exiting...Invalid urls..")
	else:
		urls = parser(base_url, nano_url)
		urls_len = len(urls)
		if not urls:
			logging("Invalid responses..")
		else:
			cnt = 0
			for url in urls:
				print("Scraping for: "+str(url.rsplit('/', 1)[-1]).upper()+"\n")
				month_sp = mk_soup(url)
				ele_text, ele_url = inner_sp_for_articles(month_sp)
				ele_url = nano_url + ele_url
				all_ele_text.apdpend(ele_text)
				all_ele_url.append(ele_url)

		all_ele_text_url = dict(zip(all_ele_text, all_ele_url))

		ELE_TXT_FILE = "ele_txt.txt"
		ELE_URL_FILE = "ele_url.txt"
		ELE_TXT_URL_FILE = "ele_txt_url.txt"
		EXPORT_CSV_FILE = "ele_txt_url.csv"

		file_write(ELE_TXT_FILE, all_ele_text)
		file_write(ELE_URL_FILE, all_ele_url)
		file_write_dict(ELE_TXT_URL_FILE, all_ele_text_url)
		export_to_csv(EXPORT_CSV_FILE, all_ele_text, all_ele_url)
		#pd_to_csv(EXPORT_CSV_FILE, all_ele_text_url)

def export_to_csv(filenm, list1, list2):
	df = pd.DataFrame(data={"Name": list1, "URL": list2})
	df.to_csv(filenm, sep=',',index=False)

def main():
	nano_url = "http://highscalability.com"
	base_url = "http://highscalability.com/all-posts/"
	parse_each_url(base_url, nano_url) 

if __name__ == '__main__':
	main()