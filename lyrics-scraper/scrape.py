from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

def get_lyrics(artist):
    """Print all lyrics for given artist on azlyrics.com.

    Takes artist name as an argument, follows all song links 
    on artist's page, and prints lyrics for each song."""

    base_url = 'http://www.azlyrics.com/'

    #Change artist name to match url format: "azlyrics.com/w/west.html"
    artist_url = 'http://www.azlyrics.com/' + artist[0] + '/' + artist + ".html"

    #Use requests library to get html from artist's page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    response = requests.get(artist_url, headers= headers)
    
    #Make the html soup object!
    soup = BeautifulSoup(response.text, "lxml")

    #Find all song links on the page and create a new html soup object for each linked page.
    #For each song page, remove irrelevant text and return lyrics.
    for song_link in soup.find_all('a', attrs={'target': '_blank'})[1:]:  
        link = urljoin(base_url, song_link['href'][3:])
        print(link)
        response = requests.get(link, headers= headers)
        soup = BeautifulSoup(response.text, "lxml")

        # Remove unnecessary text items on page
        #(desired info is in a div w/o a class or additional selectors)
        for text in soup.find_all(['a','small','script','title','span','b','h1']):
            text.decompose()

        for text in soup.select('.hidden'):
            text.decompose()

        # get remaining text (lyrics) from page:
        print((soup.get_text(strip=True, separator=" ")))


get_lyrics("gunsandroses")


