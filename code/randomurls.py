from random_words import RandomWords
from bs4 import BeautifulSoup
import requests
import webbrowser

rw = RandomWords()
words = rw.random_words(count = 1500)

# NEWS articles
for word in words:
	try:
		google_search = "https://www.google.com/search?q=" + word + "&source=lnms&tbm=nws"
		##print(google_search)
		r = requests.get(google_search)
		soup = BeautifulSoup(r.text, "html.parser")

		links = soup.find_all("h3", limit=1)
		for item in links:
			for k in item.children:

				url = k.get("href")[7:]
				
				m = requests.get(url)
				if m.status_code == 200:
					#webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)
					print(url)
	except:
		continue
	# try:
	# 	print (soup.find('cite').text + " -- " + word)
	# except:
	# 	continue






# Non news articles:


# for word in words:
# 	google_search = "https://www.google.com/search?q=" + word
# 	r = requests.get(google_search)
# 	soup = BeautifulSoup(r.text, "html.parser")
# 	print(soup.find('cite').text)