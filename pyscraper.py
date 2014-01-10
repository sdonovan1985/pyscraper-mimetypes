from bs4 import BeautifulSoup
import re
import urllib2
import httplib
import urlparse

def getMimeType(address):
  # Starting from https://stackoverflow.com/questions/1636637/i-am-downloading-a-file-using-python-urllib2-how-do-i-check-how-large-the-file
  u= urlparse.urlparse(address)
  cn= httplib.HTTPConnection(u.netloc)
#  print "Path to get", u.path, "all of u", u
  cn.request('GET', u.path)#, headers= {'User-Agent': ua})
  r= cn.getresponse()

  return (r.getheader('Content-type', '0')).split(";")[0]

def getAllLinks(website):
  pages = []
  site = urllib2.urlopen(website)
  soup = BeautifulSoup(site)
  
  pages.extend(getLinksOfType(website, soup, 'img', 'src'))
  pages.extend(getLinksOfType(website, soup, 'a', 'href'))
# for HTML5 video
  pages.extend(getLinksOfType(website, soup, 'source', 'src'))

#  for page in pages:
#    print page
  return pages

def getLinksOfType(website, soup, type, source):
  links = []
  imgs = soup.find_all(type)
  for img in imgs:
    imglink = img[source]
    if "mailto" in imglink: 
      continue
    imglink = urlparse.urljoin(website, imglink)
    links.append(imglink)
  return links

def printLinks(website):
  links = getAllLinks(website)
  for link in links:
    print link
    print getMimeType(link), ":", link

