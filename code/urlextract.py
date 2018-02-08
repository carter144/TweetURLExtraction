from bs4 import BeautifulSoup
import urllib.request as urllib2
import requests
from lxml.html import fromstring
import webbrowser


def crawl(url):
	if isinstance(url, str):
		print("STRING")
	else:
		print("UNICODE")
		url = url.decode("utf-8")

	webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

with open("inputURLs.txt", "rb") as f:
	
	for line in f:
		crawl(line.strip())

# inputs = []
# with open("goods.txt", "rb") as f:
# 	for line in f:
# 		if isinstance(line, str):
# 			pass
# 		else:
# 	 		line = line.decode("utf-8")
# 		inputs.append(line.strip())

# with open("inputURLs.txt", "rb") as k:
# 	for line in k:
# 		if isinstance(line, str):
# 			pass
# 		else:
# 	 		line = line.decode("utf-8")
# 		if line.strip() not in inputs:
# 			print(line.strip())