import urllib    
import json      

title = raw_input("Enter word to search: ")
print "Word: ",title
 
#stores the json formatted output to a variable
url = 'http://glosbe.com/gapi/translate?from=eng&dest=eng&\
format=json&phrase='+title+'&pretty=true'
 
#json representation of url is stored in variable result
result = json.load(urllib.urlopen(url)) 
 
#get the first text in "meaning" in "tuc" from result
try:
    print "Meaning: ", result["tuc"][0]["meanings"][0]["text"]
except Exception as e:
    print "Error!"
    