from bs4 import BeautifulSoup
import urllib.request as req
import time

memrise_url = "https://www.memrise.com/course/121215/barrons-800-essential-word-list-gre/"
sentences_url = "sentence.yourdictionary.com/"

mapping = dict()
combine = []

for i in range(1,81):
	url = memrise_url + str(i) + "/"
	response = req.urlopen(url)
	data = response.read()
	soup = BeautifulSoup(data,'lxml')
	for w in soup.find_all("div", class_ = "thing text-text"):
		word = w.find("div", class_ = "col_a col text")
		meaning = w.find("div", class_ = "col_b col text")
		combine.append((word.text, meaning.text))
		if word.text not in mapping:
			mapping[word.text] = meaning.text
			antimapping = dict((y, x) for x,y in mapping.items())
	time.sleep(2)
	break

with open("memrise_mapper.txt", 'a') as mfile:
	for ele in combine:
		writetotxt = str(ele[0]) + " => " + str(ele[1]) + "\n"
		mfile.write(writetotxt)