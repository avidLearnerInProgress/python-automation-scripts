import urllib3
import shutil
from bs4 import BeautifulSoup as bs


def main():
    
    ur = input("Input URL Here ")
    
    http = urllib3.PoolManager()
    
    page = http.request('GET', ur)
    
    soup = bs(page.data, 'html.parser')
    
    link = ["http:"+ls.get('href') for ls in soup.find_all('a', {"class" : "zoom"})]
    for vd in soup.find_all('source'):
        link.append('http:'+vd.get('src'))
    print(link)

    for ln in link:
        index = ln.rindex('/')
        filename = ln[index+1:len(ln)]
        with http.request('GET', ln, preload_content=False)as resp, open(filename, 'wb') as out_file:
            shutil.copyfileobj(resp, out_file)
if __name__ == "__main__":
    main()    