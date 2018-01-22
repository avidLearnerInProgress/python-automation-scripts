from pyshorteners import Shortener
import webbrowser
import clipboard
import time
import tinyurl
import urllib2

#------------------------HELPER UTILITIES--------------------

def getOnlyQRCode(shortened_url):
	url = "http://chart.apis.google.com/chart?cht=qr&chl={}&chs=120x120".format(shortened_url)
	print "\n\tQRCode is on the URL: {}".format(url)
	webbrowser.open_new_tab(url)
	time.sleep(2)


def printShortener(shortener, url):
	#print "\n\tinside print."
	try:
		getshorted = shortener.short(url)
		print "\n\tShortened url is {}".format(getshorted)
		clipboard.copy(getshorted)
		print "\n\tDone, your shortened url is on clipboard.!"
		print "\n\tLaunch your browser and use 'Command-V' OR 'Ctrl + V' to paste the link in your browser."

		time.sleep(5)

		print "\n\tWant to Fetch QRCode? press 1 else press 0"

		choice=int(input("\n\t"))

		if choice == 1:
			getQRCode(shortener,url)
		elif choice == 0:
			return
		else:
			print "Error!"
			return

	except Exception as e:
		print str(e)
	
 
def getQRCode(shortener, url):
	shortener.short(url)
	print "\n\tQRCode is on the URL: {}".format(shortener.qrcode())
	try:
		webbrowser.open_new_tab(shortener.qrcode())
		time.sleep(2)
	except Exception as e:	
		print "\n\tLaunch your browser and use 'Command-V' OR 'Ctrl + V' to paste the link in your browser."
		clipboard.copy(shortener.short(url))
		time.sleep(2)

#you could also save your qrcode locally by simply calling urllib on the image url



#----------------------- MAIN FUNCTIONS --------------------

def googleShortener(url):
	key = 'AIzaSyAkWqqAmotOf98k421TC3PetlPbeZlXoEA'
	shortener = Shortener('Google', api_key = key)
	printShortener(shortener,url)

def bitlyShortener(url):
	access_token = '03cf036ff2a4aa31b93c369af9e33478ddd44f02'
	shortener = Shortener('Bitly', bitly_token = access_token)
	printShortener(shortener,url)

def tinyurlShortener(url):
	shortened = tinyurl.create_one(url)
	print "\n\tShortened url is {}".format(shortened)
	clipboard.copy(shortened)
	print "\n\tDone, your shortened url is on clipboard.!"
	print "\n\tLaunch your browser and use 'Command-V' OR 'Ctrl + V' to paste the link in your browser."
	time.sleep(5)
	print "\n\tWant to Fetch QRCode? press 1 else press 0"
	choice=int(input("\n\t"))
	if choice == 1:
		getOnlyQRCode(shortened)
	elif choice == 0:
		return
	else:
		print "Error!"
		return

	

def isgdShortener(tourl):
	url = 'https://is.gd/create.php?format=simple&url={}'.format(tourl)
	shortened = urllib2.urlopen(url).read()
	print "\n\tShortened url is {}".format(shortened)
	clipboard.copy(shortened)
	print "\n\tDone, your shortened url is on clipboard.!"
	print "\n\tLaunch your browser and use 'Command-V' OR 'Ctrl + V' to paste the link in your browser."
	time.sleep(5)
	print "\n\tWant to Fetch QRCode? press 1 else press 0"
	choice=int(input("\n\t"))
	if choice == 1:
		getOnlyQRCode(shortened)
	elif choice == 0:
		return
	else:
		print "Error!"
		return

'''
def adflyShortener(tourl):
	UID = 18844965
	API_KEY = 'd8a2283a6bbafbe31b442776fdc108ab'
	url = 'http://api.adf.ly/api.php?key={}&uid={}&advert_type=int&domain=adf.ly&url={}'.format(API_KEY,UID,tourl)
	r = urllib2.urlopen(url).read()
	print r
'''

def main():

	print "\n\tList of URL Shortener Services:\n\t\t1. Google\n\t\t2. Bit.ly\n\t\t3. TinyURL\n\t\t4. IS.GD\n\t\t"
	try:
		choice = int(raw_input("\n\tChoose URL SHORTENER service: "))
		print "\n\tTo enter url, you can type manually in your console or else you can copy the url using 'Command-V' or 'Ctrl + V'\n\tfrom browser."
		print "\n\t1. Manually in console\n\t2. Copy from browser\t"
		urlchoice = int(raw_input("\n\tEnter choice: "))

		if urlchoice == 1:
			print "\n\tEnter url to be shortened: ",

			url = str(raw_input(""))
		elif urlchoice == 2:
			print "\tYou have five seconds..copy the url from address bar you wish to shorten!"
			time.sleep(5)
			url = clipboard.paste()
		else:
			print "\n\tInvalid Option.! Quitting.."
			time.sleep(1)
			sys.exit(0)

		if choice == 1:
			googleShortener(url)

		elif choice == 2:
			bitlyShortener(url)

		elif choice == 3:
			tinyurlShortener(url)

		elif choice == 4:
			isgdShortener(url)

		else:
			print "Invalid Service."

	except Exception as e:
		print str(e)


if __name__ == '__main__':
	main()