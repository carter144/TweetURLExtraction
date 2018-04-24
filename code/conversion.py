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
        exit()
    except requests.exceptions.Timeout:
        print("Time out error")
        exit()
    except requests.exceptions.ContentDecodingError:
        print("Decode error")
        
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
            
            # Removing non-alphanumeric characters
            # text = char_re.sub("\g<1>\g<2>", text)
            # text = right_re.sub("\g<1>", text)
            # text = left_re.sub("\g<1>", text)  
            # text = center_re.sub(" ", text)
            
            # Removing multiple spacing characters
        text = space_re.sub(" ", text)

        text = text.encode("ascii", errors="ignore").decode()
        text = preProcess(text)
            # Stripping leading and trailing spaces
        text = text.strip()
        return text
    except:
        print("Error in parsing html")
        exit()


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
    

    args = parser.parse_args()


    if args.url is not None:
        url = args.url

    html_content = scrape_link(url)
    text = parse_html(html_content)

    # Create corpus from sample data
    corpus = createCorpus("../data/url_info.csv")
    stop_words = [x.strip() for x in open('../data/stop_words.txt','r').read().split('\n')]
    vectorizer = TfidfVectorizer(stop_words=stop_words, min_df=0.10, max_df=0.90)
    K = vectorizer.fit_transform(corpus)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(K, bool_array, test_size = 0.2)

    #Convert single url to tfidf vector
    idf_array = vectorizer.transform([text])

    # Train the data
    clf=RandomForestClassifier(max_depth=19, n_estimators=7, max_features="auto", min_samples_leaf=1, random_state=15, n_jobs=-1)
    clf.fit(X_train, y_train)

    # Predict the input url
    print(clf.predict(idf_array))



