import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")
import youtube_dl
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import time


#todo
#integrate progress bar
#add playlist feature
#add other features..

DEVELOPER_KEY = "AIzaSyDKpuaw516j1wI8ZGqh-AS7xOFmim86vL4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

  

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)


def getProgressBar():
  toolbar_width = 80
  # setup toolbar
  sys.stdout.write("[%s]" % (" " * toolbar_width))
  sys.stdout.flush()
  sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

  for i in xrange(toolbar_width):
      time.sleep(0.1) # do real work here
      # update the bar
      sys.stdout.write("-")
      sys.stdout.flush()
  sys.stdout.write("\n")



def hook(ph):
  print("\n")
  sys.stdout.write('Downloading...')
  if ph['status'] == 'downloading':

    #sys.stdout.write('Downloading... ETA: ' + str(ph["eta"]) + " seconds\n")
    sys.stdout.flush()
    percent = float(ph['downloaded_bytes'])/float(ph['total_bytes']) * 100.0
    sys.stdout.write(str(round(percent,0))+" %")
    sys.stdout.flush()
    
  elif ph['status'] == 'finished':
    sys.stdout.write('\nDownload complete\n')
    sys.stdout.flush()


ydl_opts = {
    'format': 'bestvideo',
    'outtmpl': '%(title)s.%(ext)s',
    'progress_hooks':[hook],  
    'logger': MyLogger()
}

def youtube_search(search_query, max_results):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
  search_response = youtube.search().list(
    q=search_query,
    part="id,snippet",
    maxResults=max_results
  ).execute()

  search_videos = []
  videos_id = []
  videos_title = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos_id.append(search_result["id"]["videoId"])
      videos_title.append(search_result["snippet"]["title"])

  #tabular_list = []
  #headers = ['No.' , 'Title', 'VideoId']
  i = 0
  print "Videos:\n" 
  for vid in videos_title:
    #tabular_list.append([i+1, videos_title[i], videos_id[i]])
    print "%s -- (%s)"%(i+1, videos_title[i]) 
    i += 1

  print "Enter video number to download: "
  choice = int(raw_input(" "))
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(['http://www.youtube.com/watch?v=' + videos_id[choice]])
      print("\tDone")
  #print tabulate(tabular_list, headers, tablefmt="fancy_grid")


if __name__ == "__main__":
  
  search_query = str(raw_input("Enter search query: "))
  max_results = int(raw_input("Enter max results to be displayed: "))

  try:
    youtube_search(search_query, max_results)
    #getProgressBar()
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)