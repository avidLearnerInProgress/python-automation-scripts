from bs4 import BeautifulSoup
import urllib.request as req
import time

memrise_url = "https://www.memrise.com/course/121215/barrons-800-essential-word-list-gre/"
sentences_url = "http://sentence.yourdictionary.com/"

mapping = dict()
combine = []
glob_s = []

sentence_map = dict()

def get_sentences(ur):
	url = ur
	print(url)
	response = req.urlopen(url)
	data = response.read()
	soup = BeautifulSoup(data, 'lxml')
	sentences = []
	for s in soup.find_all("li", class_ = 'voting_li'):
		sentence = s.find("div", class_ = 'li_content')
		#print(sentence.text)
		sentences.append(sentence.text)
	return sentences

for i in range(1,81):
	url = memrise_url + str(i) + "/"
	response = req.urlopen(url)
	data = response.read()
	soup = BeautifulSoup(data,'lxml')
	for w in soup.find_all("div", class_ = "thing text-text"):
		word = w.find("div", class_ = "col_a col text")
		meaning = w.find("div", class_ = "col_b col text")
		sentence = sentences_url + word.text
		sentences = get_sentences(sentence)
		sentences = sentences[:4]
		
		combine.append((word.text, meaning.text))
		#glob_s.append(sentences)
		sentence_map[word.text] = sentences

		if word.text not in mapping:
			mapping[word.text] = meaning.text
			antimapping = dict((y, x) for x,y in mapping.items())
	time.sleep(3)

with open("memrise_mapper.txt", 'r') as f:
	contents = f.read()

with open("memrise_mapper.txt", 'a') as mfile:
	for ele in combine:
		if ele[0] in contents:
			print("Mapping already exists.")
		else:
			writetotxt = str(ele[0]) + " => " + str(ele[1]) + "\n"
			#mfile.write("!-------------------!\n")
			mfile.write(writetotxt)
			if ele[0] in sentence_map.keys() and len(sentence_map[ele[0]]) != 0:
				for s in sentence_map[ele[0]]:
					mfile.write(s + "\n")
				mfile.write("!-------------------!\n\n")
			else:
				mfile.write("No sentences.. :( \n")
				mfile.write("!-------------------!\n\n")