from bs4 import BeautifulSoup
import requests
import urllib2



quote_page = "http://www.bloomberg.com/quote/SPX:IND"
soup = BeautifulSoup(urllib2.urlopen(quote_page), "html.parser")
print (soup.find("h1", attrs = {"class" :"name"}).string)
print(soup.find("div", attrs = {"class":"price"}).string)


"""from bs4 import BeautifulSoup
import requests
import urllib2



quote_page = "http://www.nasdaq.com/symbol/nvda"
soup = BeautifulSoup(urllib2.urlopen(quote_page), "html.parser")
#print (soup.find("h1", attrs = {"class" :"name"}).string)
print(soup.find("div", attrs = {"class":"qwidget-dollar"}).string)
print(soup.find("div", attrs = {"id" : "qwidget_percent"}).string)

"""

