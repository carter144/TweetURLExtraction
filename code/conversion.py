import argparse
import pandas
import requests
import bs4
from requests.exceptions import ConnectionError
import newspaper
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
import nltk
import csv
import string
import pickle
import sys
from bs4 import BeautifulSoup
from string import punctuation
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score



bool_array = []

def scrape_link(url):

    try:
        resp = requests.get(url, timeout = 500, stream=True)

        soup = bs4.BeautifulSoup(resp.content, "lxml")
        status_code = resp.status_code
        title = ""
        title_el = soup.find("title")
        if title_el is not None:
            title = soup.find("title").text
        
    except ConnectionError as e:
        print("error in connection")
        return ""
    except requests.exceptions.Timeout:
        print("Time out error")
        return ""
    except requests.exceptions.ContentDecodingError:
        return ""
        
    return soup.html

def preProcess(text):
    # Create lemmatizer
    lemmatizer = WordNetLemmatizer()
    l = LancasterStemmer()
    # Tokenize to sentences into a list
    sent_tokenize_list = sent_tokenize(text)

    # An array to store the words as tokens
    tokenized_words = []

    # Since sent_tokenize_list is now a list of strings, we have to iterate through each one and split on spaces to get individual words
    for sentence in sent_tokenize_list:
        
        k = ' '.join(filter(None, (word.strip(punctuation) for word in sentence.split())))
        for words in k.split():
            
            if "." in words:
                words_re = re.compile("(.+)\.|\?")
                m = words_re.search(words).group(1)
                words = m
            k = lemmatizer.lemmatize(words.lower())
            j = l.stem(k)
            tokenized_words.append(j)
            
    # Itreates through each word to create final stirng
    final = ' '.join(str(x) for x in tokenized_words)

    return final

def parse_html(html):
    try:
        url_re = re.compile("https{0,1}://[^\s]+")
        url2_re = re.compile("[a-z0-9\.]+\.[a-z0-9\.]+/[^\s]*")
        space_re = re.compile("[\s]{2,}")

        html = html.encode("ascii", errors="ignore")
        text = newspaper.fulltext(html)
        
        sent = text.encode('ascii', errors='ignore')
        sent = str(sent).replace("r\\", "")
        sent = str(sent).replace("n\\", "")
        sent = str(sent).replace("\\", "")
        text = sent

        t, d = MosesTokenizer(), MosesDetokenizer()
        tokens = t.tokenize(text)
        detokens = d.detokenize(tokens)
        text = " ".join(detokens)
            # Removing URLs
        text = url_re.sub(" ", text)
        text = url2_re.sub(" ", text)
            
        # Removing multiple spacing characters
        text = space_re.sub(" ", text)

        text = text.encode("ascii", errors="ignore").decode()
        text = preProcess(text)
            # Stripping leading and trailing spaces
        text = text.strip()
        return text
    except Exception as e:
        return ""


def createCorpus(csvFile):
    corpus_array = []
    
    csv_fp = open(csvFile, "r", encoding="utf8")
    reader = csv.reader(csv_fp)
    rows = [row for row in reader]
    csv_fp.close()
   
    trues = 0
    falses = 0

    for row in rows:
        corpus_array.append(row[4])
        if row[1].lower() == "false" or row[2] != "200" or len(row[4]) == 0:
            bool_array.append(0)
            falses = falses + 1
        else:
            bool_array.append(1)
            trues = trues + 1
    print("Number of good links: " + str(trues))
    print("Number of bad links: " + str(falses))
    
    return corpus_array



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-u', '--url', help="single url")
    parser.add_argument('-f', '--file', help="input file for list of urls")
    

    args = parser.parse_args()
    vectorizer = pickle.load(open("vectorizer.pickle", "rb"))
    clf = pickle.load(open("model.pickle", "rb"))

    if args.url is not None and args.file is None:
        url = args.url

        html_content = scrape_link(url)
        text = parse_html(html_content)
        idf_array = vectorizer.transform([text])

        # Predict the input url
        print(clf.predict_proba(idf_array))
        print(clf.predict(idf_array))
    if args.file is not None:
        file_path = args.file
        with open(file_path, "r", encoding="utf8") as f:
            for line in f:
                url = line.strip()
                html_content = scrape_link(url)
                if (html_content == ""):
                    continue
                text = parse_html(html_content)
                if (text == ""):
                    continue
                idf_array = vectorizer.transform([text])
                if (clf.predict(idf_array) == 1):  # 1 is a good link
                    print(url)


    # [1, 0] bad
    # [0, 1] good



