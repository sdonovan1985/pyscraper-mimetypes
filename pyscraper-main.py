from bs4 import BeautifulSoup
import re
import urllib2

def downloadSite(website):
  print "Downloading", website
  soup = BeautifulSoup(urllib2.urlopen(website))
  imgs = soup.find_all('img')
  imgcount = 0;
  for img in imgs:
    #print img
    imglink = img['src']
    #print imglink
    if imglink[0] == '/':
      imglink = website + imglink
    print "  Image", imgcount, " link is ", imglink
    urllib2.urlopen(imglink)
    imgcount += imgcount
  print "Finished   ", website
