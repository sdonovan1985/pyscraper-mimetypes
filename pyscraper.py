from bs4 import BeautifulSoup
import re
import urllib2
import httplib
import urlparse
import time
import datetime

def getRequestData(address):
  # Starting from https://stackoverflow.com/questions/1636637/i-am-downloading-a-file-using-python-urllib2-how-do-i-check-how-large-the-file
  requestData = {'address':address}
  u = urlparse.urlparse(address)
  cn= httplib.HTTPConnection(u.netloc)
#  print "Path to get", u.path, "all of u", u
  cn.request('HEAD', u.path)#, headers= {'User-Agent': ua})
  r = cn.getresponse()
  
  size = -1
  mime = "unknown"
  try:
    mime = (r.getheader('Content-type', '0')).split(";")[0]
    size = int(r.getheader('Content-Length', '0'))
        
  except ValueError:
    cn.request('GET', u.path)#, headers= {'User-Agent': ua})
    r = cn.getresponse()
    mime = (r.getheader('Content-type', '0')).split(";")[0]
    size = int(r.getheader('Content-Length', '0'))

  requestData['size'] = size
  requestData['mime-type'] = mime
  #from https://stackoverflow.com/questions/13890935/timestamp-python
  requestData['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
  return requestData


def getMimeType(address):
  # Starting from https://stackoverflow.com/questions/1636637/i-am-downloading-a-file-using-python-urllib2-how-do-i-check-how-large-the-file
  u= urlparse.urlparse(address)
  cn= httplib.HTTPConnection(u.netloc)
#  print "Path to get", u.path, "all of u", u
  cn.request('GET', u.path)#, headers= {'User-Agent': ua})
  r= cn.getresponse()

  return (r.getheader('Content-type', '0')).split(";")[0]


def getSize(address):
  # Starting from https://stackoverflow.com/questions/1636637/i-am-downloading-a-file-using-python-urllib2-how-do-i-check-how-large-the-file
  u= urlparse.urlparse(address)
  cn= httplib.HTTPConnection(u.netloc)
#  print "Path to get", u.path, "all of u", u
  cn.request('GET', u.path)#, headers= {'User-Agent': ua})
  r= cn.getresponse()

  return long(r.getheader('Content-length', '0'))


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

def saveOffSiteDetails(sites):
  details = []
  for site in sites:
    #this does make the request twice... not the best, but not horrible
    details.append(getRequestData(site))
  
#  for detail in details:
#    print detail['mime-type'], detail['size'], detail['address']
  return details
