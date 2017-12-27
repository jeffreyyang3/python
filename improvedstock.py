from bs4 import BeautifulSoup
import requests
import urllib2



quote_page = "http://www.nasdaq.com/symbol/" + raw_input("whats symbol of stock u want learn about?? ")
soup = BeautifulSoup(urllib2.urlopen(quote_page), "html.parser")
#print (soup.find("h1", attrs = {"class" :"name"}).string)
"""if (soup.find("div", attrs = {"id" : "qwidget_percent"}).find("Green", beg=0, end=len("Green")) == -1):
	dank = "-"
else:
	dank = "+"
"""

print(soup.find("div", attrs = {"id" : "qwidget_pageheader" }).text + ":")
print(soup.find("div", attrs = {"class":"qwidget-dollar"}).text)
print(soup.find("div", attrs = {"id" : "qwidget_percent"}).text)








