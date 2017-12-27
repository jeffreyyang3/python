from bs4 import BeautifulSoup
import requests
import urllib2



quote_page = "http://finance.google.com/finance?q=NASDAQ:NVDA"
soup = BeautifulSoup(urllib2.urlopen(quote_page), "html.parser")
print(soup.find("span" , "pr").text)
for i in soup.find_all("span" , "chg"):
	print i.text
a = []
b = []
for i in soup.find_all("td", "val"):
	b.append(i.text)

for i in soup.find_all("td" , "key"):
	a.append(i.text)

for i in range(0,10):
	print a[i] + b[i]