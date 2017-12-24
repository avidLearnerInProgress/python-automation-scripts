from bs4 import BeautifulSoup
import pdfkit
import time,os

#helper functions
def absolute_path_shortner(absolute_path):  #returns filename after removing directory name
    head,tail=os.path.split(absolute_path)
    return tail

def countLines(filename):
	num_lines=sum(1 for line in open(filename))
	return num_lines

def checkFileExists(filename,i):
	pdfFileName=os.getcwd()+"\\"+str(i)+". "+filename+".pdf"
	print(pdfFileName)
	if os.path.exists(pdfFileName):
		return True
	else:
		return False

#invocation functions
def extractFromBookmarks():
	inFile="data.txt"
	outFile="extracted.txt"
	with open(inFile,'r',encoding='utf-8') as f:
		s=f.read()
		f.close()
		result=""
		e=open(outFile,'w')
		soup=BeautifulSoup(s,'lxml')
		for div in soup.find_all('div',attrs={'class':'postArticle-content'}):
			result+=(div.find('a')['href'])
			result+="\n"
			e.write(result)
			result=""
	e.close()
	time.sleep(2)
	trimExtractedFile()


def trimExtractedFile():
	outFile=open("trimmed.txt","w")
	inFile="extracted.txt"
	with open(inFile,"r") as fp:
		line=fp.readline()
		cnt=1
		while line:
		#outFile.write(str(cnt)+" ")
			trimmedLine=line.split("?")[0]
			outFile.write(trimmedLine)
			outFile.write("\n")
			line=fp.readline()
			cnt+=1
	outFile.close()
	time.sleep(2)
	generatePdfFromUrl()	

def generatePdfFromUrl():
	options = {
            'quiet':'',
            'page-size':'A4',
            'dpi':300,
            'disable-smart-shrinking':'',
        }

	path_wkthmltopdf=b'C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  #can also be done via Envt. Settings in windows!
	config=pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	inFile="trimmed.txt"
	count=countLines(inFile)
	#print(count)
	with open(inFile,"r") as url_read:
		for i in range(2,count-209):
			urlLine=url_read.readline()
			trimmedUrlLineList=urlLine.rsplit('/',1)
			trimmedUrlLineWithoutStrip=str(trimmedUrlLineList[-1])
			trimmedUrlLine=trimmedUrlLineWithoutStrip.rstrip()
			#print(trimmedUrlLine)  #phew! finally extracted the url content!!
			if checkFileExists(trimmedUrlLine,i)==True:
				print("Pdf Already Generated")
			else:
				print("Generating pdf for URL:\n"+urlLine)
				#pdfkit.from_url(url=urlLine, output_path=str(i)+". "+trimmedUrlLine+'.pdf',configuration=config,options=options)
				time.sleep(3)
			i=i+1

if __name__=="__main__":
	extractFromBookmarks()
	