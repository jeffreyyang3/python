from bs4 import BeautifulSoup
import requests
import urllib2



quote_page = "http://finance.google.com/finance?q=NASDAQ:NVDA"
soup = BeautifulSoup(urllib2.urlopen(quote_page), "html.parser")
for i in soup.find_all("span" , "chg"):
	print i.text