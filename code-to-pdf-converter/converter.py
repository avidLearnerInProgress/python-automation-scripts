from subprocess import Popen
import os
import easygui
from PyPDF2 import PdfFileReader, PdfFileMerger , PdfFileWriter
import glob

def absolute_path_shortner(absolute_path):
		head,tail=os.path.split(absolute_path)
		return tail

def get_curr_path(absolute_path):  #os.getcwd()
		head,tail=os.path.split(absolute_path)
		return head

'''
 autumn
 borland
 bw
 colorful
 default
 emacs
 friendly
 fruity
 igor
 manni
 monokai
 murphy
 native
 paraiso-dark
 paraiso-light
 pastie
 perldoc
 rrt
 tango
 trac
 vim
 vs
 xcode

'''

def fileNameExtension(fileName):
	extension = os.path.splitext(fileName)[0]
	return extension


def makeDir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
'''
print(os.getcwd())
print(__file__)
print(os.path.realpath(path))
dir = os.path.dirname(os.path.dirname(__file__)) ## dir of dir of file
## once you're at the directory level you want, with the desired directory as the final path node:
dirname1 = os.path.basename(dir) 
dirname2 = os.path.split(dir)[0] ## if you look at the documentation, this is exactly what os.path.basename does
print(dirname1)
print(dirname2)
'''

def mergeIntoOnePDF(path):
    f=path+"\\"
    pdf_files=[fileName for fileName in os.listdir(f) if fileName.endswith('.pdf')]
    print(pdf_files)
    merger=PdfFileMerger()
    for filename in pdf_files:
        merger.append(PdfFileReader(os.path.join(f,filename),"rb"))
    merger.write(os.path.join(f,"merged_full.pdf"))
        
def generateMultiplePDF(path):
    for file in os.listdir(path):
        #print(file)
        current_file=os.path.join(path, file)
        #print(current_file)
        current_absolute_file=absolute_path_shortner(current_file)
        #print(current_absolute_file)
        if os.path.exists(current_file):
            inputFilename=current_absolute_file
            #print(get_curr_path(inputFilename))
            if inputFilename.endswith('.cpp'):   #basically u can append further whatever files extensions you need to convert
                last_extracted_folder=os.path.basename(os.path.normpath(path))
                #print(last_extracted_folder)
                outputDirectory=path+'_'+last_extracted_folder
                makeDir(outputDirectory)
                styleName="emacs"
                a=" "+"-S="+styleName+" -l -s A4 "+path+inputFilename+" "
                b=outputDirectory+"\\"+fileNameExtension(inputFilename)+".pdf"
                c=a+b
                #print(c)
                Popen('python code2pdf.py'+c,shell=True)
    return outputDirectory
    
    

def main():
    print("Choose directory:")
    choosen_path=easygui.diropenbox("Path containing .cpp files:")
    try:
        get_path=choosen_path+'\\'
        newObtainedPath=generateMultiplePDF(get_path)
        mergeIntoOnePDF(newObtainedPath)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()