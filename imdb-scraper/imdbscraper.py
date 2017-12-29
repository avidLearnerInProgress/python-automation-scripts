from bs4 import BeautifulSoup
import urllib.request as req
from tabulate import tabulate

def getResponse(url):
	response = req.urlopen(url)
	data = response.read()
	soup = BeautifulSoup(data, "lxml")
	#print(soup.prettify("utf-8"))
	return soup

def selectChoice():

	'''options = {
	1: ('top'),
	2: ('moviemeter'),
	3: ('top-english-movies'),
	4: ('toptv'),
	5: ('tvmeter'),
	6: ('bottom'),
	7: ('boxoffice')
	}
	'''
	options_map = {
		1: ('Top movies' , 'top'),
		2: ('Most Popular Movies' , 'moviemeter'),
		3: ('Top English Movies' , 'top-english-movies'),
		4: ('Top TV Shows' , 'toptv'),
		5: ('Most Popular TV Shows' , 'tvmeter'),
		6: ('Low Rated Movies', 'bottom'),
		7: ('Top Box Office collection', 'boxoffice')
	}

	for i,option in enumerate(options_map,1):
		print("{}) {}".format(i,options_map[option][0]))

	choice = int(input('\nChoice please..\n'))
	while(choice<1 or choice>len(options_map)):
		print('Wrong choice, enter again..')
		choice = int(input('\nChoice please..\n'))
	return options_map[choice][1]

def getData(base_url, option):
	complete_url = base_url + option
	soup = getResponse(complete_url)
	card_list = soup.find_all('span',{'class':'media-body media-vertical-align'}) #material card list
	result = []
	count = 1
	for card in card_list:
		try:
			name = card.find('h4').text.replace("\n"," ").lstrip("0123456789.- ")  #removes order indexes for movies 1,2,3,4,...
		except: 
			pass
		try:
			rating = card.find('p').text.strip()
		except:
			pass
		result.append([count,name,rating]) 
		count += 1
	print(tabulate(result, headers=["Index", "Name", "Ratings"],  tablefmt="grid"))

def main():
	base_url = "http://m.imdb.com/chart/"
	choice = selectChoice()
	#print(choice)
	getData(base_url, choice)
	
if __name__ == '__main__':
	main()


'''
#table formats
- "plain"
- "simple"
- "grid"
- "fancy_grid"
- "pipe"
- "orgtbl"
- "jira"
- "presto"
- "psql"
- "rst"
- "mediawiki"
- "moinmoin"
- "youtrack"
- "html"
- "latex"
- "latex_raw"
- "latex_booktabs"
- "textile"
'''