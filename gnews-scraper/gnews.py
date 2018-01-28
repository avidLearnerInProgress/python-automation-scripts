import urllib2
from xml.dom.minidom import parseString

def get_google_new_results( term, count ):
    results = []
    obj = parseString( urllib2.urlopen('http://news.google.com/news?q=%s&output=rss' % term).read() )
    items = obj.getElementsByTagName('item') # Get each item
    for item in items[:count]:
        t,l = '', ''
        for node in item.childNodes:
            if node.nodeName == 'title':
                t = node.childNodes[0].data
            elif node.nodeName == 'link':
                l = node.childNodes[0].data
        results.append( (t,l) )
    return results


print "Enter term to scrape from"
x = str(raw_input(""))

items = get_google_new_results( x, 50 )
for title,link in items:
	print title, ' ', link, '\n'