import os
from os import system
import urllib,sys,time,string,random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#helper functions
def openFolder(userDirectory):
    os.system("explorer " +userDirectory)

def createDirectory(foldername):
    directory=foldername+"pics"
    system("mkdir "+directory)
    system("cd "+directory)
    return directory

def getDirectory(foldername):
    directory=foldername+"pics"
    return directory


#invocation function
def downloadInstagramPics(handle):

    seleniumDriver=webdriver.Chrome("C:/Users/admin/Downloads/chromedriver_win32/chromedriver.exe") #can be done using envt. settings as well
    seleniumDriver.set_window_size(1024,768)

    #isPaging=True #Paging is enabled
    base_url="https://www.instagram.com/"
    user_url=base_url+handle
    try:
        seleniumDriver.get(user_url)
    except Exception as e:
        print "Error: "+e
        quit()
    time.sleep(1)
    print "retrieve images.."
    x=retrievePics(seleniumDriver,100,handle) #func call!
    if x==1:
        seleniumDriver.quit()
    else:
        print "Error fetching images, try later!"

#function for retrieving images
def retrievePics(driver,scrollTimes,handle):
    #images=driver.find_elements_by_css_selector("._ovg3g")

    #20 seconds !! for allowing user to click on 'load more' 
    time.sleep(20)
    print "Go to Browser and click on load more please.."
    #create directory for storing images 
    userDirectory=createDirectory(handle)
    #make all of the images appear #landing to bottom of page.
    for i in range(scrollTimes):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.1)

    #find images on the site
    images=driver.find_elements_by_tag_name("img");    
    counter=0 #counter for image names
    #iterate through all of the images
    for image in images:
        imageSrc=image.get_attribute('currentSrc')
        print imageSrc
        #save images to the userDirectory folder,as counter.png
        urllib.urlretrieve(imageSrc,"./"+userDirectory+"/" +str(counter)+".png")
        counter+=1
    time.sleep(1) #formality.. :p
    return 1


#main function
if __name__=="__main__":
    userHandle=str(raw_input("Enter instagram handle of user to fetch all images:"))
    _d_=os.getcwd()+"\\"+getDirectory(userHandle)
    #print _d_
    if os.path.exists(_d_):
        print 'Folder already exists.! Check to see if images are downloaded already.'
        time.sleep(1)
        quit()
    else:    
        downloadInstagramPics(userHandle)
        print "\n"
        print "Successfully downloaded all images of "+userHandle
        openFolder(_d_)

