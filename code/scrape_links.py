import pandas
import requests
import bs4
from requests.exceptions import ConnectionError

scraped = pandas.read_csv("../data/scraped.csv")

url_fp = open("../data/converted.txt", "r")
unlabeled = url_fp.read().splitlines()
url_fp.close()

while len(unlabeled) > 0:
    url = unlabeled.pop()
    print("Grabbing %s" % url)
    try:
        resp = requests.get(url, timeout = 5)
        soup = bs4.BeautifulSoup(resp.content, "lxml")
        status_code = resp.status_code
        title = ""
        title_el = soup.find("title")
        if title_el is not None:
            title = soup.find("title").text
        scraped.loc[len(scraped)] = [url,status_code,title,soup.html,""]
    except ConnectionError as e:
        scraped.loc[len(scraped)] = [url,"ConnectionError","","",""]
    except requests.exceptions.Timeout:
        scraped.loc[len(scraped)] = [url,"Timeout","","",""]
    except requests.exceptions.ContentDecodingError:
        scraped.loc[len(scraped)] = [url,"ContentDecodingError","","",""]
        
scraped.to_csv("../data/url_info.csv", index = False)