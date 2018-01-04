# -*- coding: utf-8 -*-
import urllib.request, re, os, sys, subprocess, short_url
from bs4 import BeautifulSoup
from tabulate import tabulate

def openWebPage(url):
    if sys.platform == "win32":
        os.startfile(url)
    else:
        process ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([process, url])

def getResponseFromServer():
    response = urllib.request.urlopen('http://www.espncricinfo.com/ci/engine/match/index.html?view=live')
    if(response == None):
        print("No Internet Connection !!")
    else:
        return extractData(response)

def getDataSoup(response):
    page_source = response.read()
    soup = BeautifulSoup(page_source, "html.parser")
    return soup

def extractData(response):
	soup = getDataSoup(response)
	matches = soup.find('section',{'id':'live-match-data'})
	match_scorecard = []
	first_innings = []
	second_innings = []
	match_status = []
	#finds all the section tags and its contents having class default-match-block
	for match in matches.find_all('section',{'class':'default-match-block'}):	
		#find a tags inside the section tag
		match_info = match.find('a') 
		#if we check on cricinfo, we will see there is only one anchor tag having parent element as span, hence its easy to scrape
		if match_info.parent.name == 'span':
			scorecard = str(match_info['href'])		
			match_scorecard.append(scorecard)
		first_score = match.find('div',{'class':'innings-info-1'}).get_text()
		first_innings.append(first_score)
		second_score = match.find('div',{'class':'innings-info-2'}).get_text()
		second_innings.append(second_score)
		status = match.find('div',{'class':'match-status'})
		status_info = status.find('span').get_text()
		match_status.append(status_info[0:75])
	return first_innings, second_innings, match_status, match_scorecard

def tabulateResults(first_innings,second_innings,match_status,match_scorecard):
	t = []
	for i in range(len(first_innings)):
	    element = []
	    element.append(i)
	    element.append(first_innings[i])
	    element.append(second_innings[i])
	    element.append(match_status[i])
	    t.append(element)
	print(tabulate(t,headers=["Index","First Innings","Second Innings","Match Status"]))

def main():
	first_innings, second_innings, match_status, match_scorecard = getResponseFromServer()
	tabulateResults(first_innings,second_innings,match_status,match_scorecard)
	length = len(first_innings)
	input_index = int(input("Choose option: 0-"+str(length-1) + " to view scorecard OR press " + str(length) + " to exit : "))
	if(input_index == length):
		sys.exit(1)
	else:
		openWebPage(match_scorecard[input_index])

if __name__ == "__main__":
	main()