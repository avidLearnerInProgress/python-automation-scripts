from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import os

def openWrittenText(writtenFile):  #comment this function if not on windows 
    os.system("notepad.exe "+writtenFile)

def absolute_path_shortner(absolute_path):  #same as os.getcwd() returns filename after removing directory name
    head,tail=os.path.split(absolute_path)
    return tail
    
def writeToText(text,filename):  #writes data into text file with same name. (8280.pdf.txt)
    filename+=".txt"
    with open(filename,"w") as f:
        f.write(text)   
    f.close()
    openWrittenText(filename)
    
def convertPdfToText(path):  #converts all pdf pages to text
    rsrcmgr=PDFResourceManager()
    retstr=StringIO()
    codec='utf-8'
    laparams=LAParams()
    device=TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp=file(path, 'rb')
    filename=path
    interpreter=PDFPageInterpreter(rsrcmgr, device)
    maxpages=0
    caching=True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password="",caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    writeToText(text,absolute_path_shortner(path))
      
 
if __name__ == "__main__":
    current_file='october17.pdf'
    current_txt_file='october17.pdf.txt'
    if os.path.exists(current_txt_file): # to check if the pdf file has already been converted to text file.
        print "Pdf already converted"
    else:
        convertPdfToText('october17.pdf')
        
             
#todo remaining
'''
support multiple file conversion.
i.e. scan a directory and get all pdf files within it and convert them.  
Will do this after NS paper!.
'''
    