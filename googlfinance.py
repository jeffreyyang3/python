from bs4 import BeautifulSoup
import requests
import urllib2

#quote_page = "http://www.nasdaq.com/symbol/" + raw_input("whats symbol of stock u want learn about?? ")

quote_page = "http://finance.google.com/finance?q=" + raw_input("Enter the symbol of a stock you want to learn more about: ")
soup = BeautifulSoup(urllib2.urlopen(quote_page), "html.parser")
print("price: " + soup.find("span" , "pr").text)
print("price change:")
for i in soup.find_all("span" , "chr"):
	print i.text
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
