import os
from os import system
import urllib,sys,time,string,random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

'''
The purpose of this script is to fetch images belonging to all answers for a particular question from quora.
I used the question, 'What are best motivational pictures?' as it has thousands of images.
Did it out of curiosity, just for fun :p
Selenium is fucking awesome !!!
'''

#note: use script at your risk.!
#according to quora policies as mentioned in their robots.txt file, scraping of answers is prohibited


#helper functions
def openFolder(userDirectory):
	os.system("explorer " + userDirectory)

def createDirectory(folderName):
	directory = folderName + "Images"
	system("mkdir " + directory)
	system("cd " + directory)
	return directory

def getDirectory(folderName):
	directory = folderName + "Images"
	return directory

#invoking functions
def downloadQuoraImagesFromAnswers(questionURL):
	seleniumDriver = webdriver.Firefox()
	seleniumDriver.set_window_size(1024,768)
	q_url = questionURL
	try:
		seleniumDriver.get(q_url)
	except Exception as e:
		print "Error" + str(e)
		quit()
	
	time.sleep(1)
	x = retrieveImages(seleniumDriver, 100, q_url)
	if x == 1:
		seleniumDriver.quit()
	else:
		print "Error fetching images, try later!"
		seleniumDriver.quit()
	
def retrieveImages(driver, scrollTimes, questionURL):

	time.sleep(1) 
	#create directory for storing images 
	userDirectory = createDirectory("answer") 

	#count answer length
	total_answers = str(driver.find_element_by_class_name("answer_count").text.split(" ")[0])
	print "Total answers : ", total_answers
	print "Loading images:" 
	print "Keep calm, sit back and enjoy :p" 
	#illogical
	#__________________________________________________________________________________________________
	'''get_number = total_answers.rsplit("+")
	get_int_number = int(get_number[0])
	print get_int_number
	'''

	'''flag = True
	while flag:  #alternate implementation of goto :p
		try:
			get_user_input=int(raw_input("Enter number of times you want to scroll to bottom of page: "))
		except Exception as e:
			print "Errors: " + e
		if get_user_input > get_int_number:
			print "The total answers are less than your input, please enter valid input:"
		else:
			flag = False
	'''
	#__________________________________________________________________________________________________

	for i in range(scrollTimes):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #scolls down after display scrollheight is completed
		# increase time.sleep() to do scraping safely.
		time.sleep(0.5)  
		
	driver.execute_script("window.scrollTo(0, 0);")	 #useful for user to get back to top of the page
	
	#Fuck selenium Ain't working ; 
	#__________________________________________________
	'''images=[]
	images=driver.find_elements_by_tag_name("img")
	for image in images:
		imageSrc=image.get_attribute('src')
        print imageSrc
	'''
	#_________________________________________________

	#resolving back to beautifulSoup
	soup=BeautifulSoup(driver.page_source,"html.parser") #take html pagesource and prepare soup from it
	#print soup.prettify("utf-8")
	images = []
	images = soup.find_all("img",{"class":["landscape","ui_qtext_image","zoomable_in_feed"]})
	counter = 0
	cntt = 0
	imageSrc = ""
	for image in images:
		imageSrc = image.get('src')
		print "Loading img: " + str(cntt)
		print imageSrc.strip().split('/')[-1].strip()
		#save images to the userDirectory folder,as counter.png
		urllib.urlretrieve(imageSrc, "./"+userDirectory+"/" +str(counter)+".png")
		cntt += 1
		counter += 1
	time.sleep(1)
	return 1
	# scraping text contents from answer is also easy, class is pagedlist_item
	# will do later

	
if __name__ == '__main__':

	question = str(raw_input("Input question: "))
	_d_ = os.getcwd()+"\\"+getDirectory("answer")
	print "\n"
	print _d_
	if os.path.exists(_d_):
		print 'Folder already exists.! Check to see if images are downloaded already.'
		time.sleep(1)
		quit()
	else:   
		#downloadQuoraImagesFromAnswers(question)
		print " Images Downloaded Successfully"