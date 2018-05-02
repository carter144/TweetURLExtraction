from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import pandas
import requests
import bs4
import re
import newspaper
from requests.exceptions import ConnectionError
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from string import punctuation
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
from nltk.stem.lancaster import LancasterStemmer

# Global variables
bool_array = []
scraped = pandas.DataFrame(columns = ["url","good_link","status_code","title","content"])

# Scrapes a provided list of links and obtains the HTML of each
def scrape_links(links, relevant, verbose = False):
    global scraped
    while len(links) > 0:
        url = links.pop()
        if verbose:
            print("Grabbing %s" % url)
        try:
            resp = requests.get(url, timeout = 5)
            soup = bs4.BeautifulSoup(resp.content, "lxml")
            status_code = resp.status_code
            title = ""
            title_el = soup.find("title")
            if title_el is not None:
                title = soup.find("title").text.strip()
            scraped.loc[len(scraped)] = [url,relevant,status_code,title,str(soup.html)]
        except ConnectionError as e:
            scraped.loc[len(scraped)] = [url,False,"ConnectionError","",""]
        except requests.exceptions.Timeout:
            scraped.loc[len(scraped)] = [url,False,"Timeout","",""]
        except requests.exceptions.ContentDecodingError:
            scraped.loc[len(scraped)] = [url,False,"ContentDecodingError","",""]
            
# Function to extract the text from the html of each article
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

# Normalizes the given text
def normalize_text(html):
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

# Creates the document corpus from the supplied CSV
def createCorpus(extracted_df):
    global bool_array
    corpus_array = []
   
    trues = 0
    falses = 0

    for index, row in extracted_df.iterrows():
        corpus_array.append(row.norm_text)
        if row.good_link:
            bool_array.append(1)
            trues = trues + 1
        else:
            bool_array.append(0)
            falses = falses + 1
            
    print("Number of relevant links: " + str(trues))
    print("Number of not relevant links: " + str(falses))
    
    return corpus_array

# Runs if invoked directly from the command line
if __name__ == "__main__":
    # Defining arguments to parse for
    parser = argparse.ArgumentParser(description='Generates a classifier model from training data')
    parser.add_argument("-v", "--verbose", help="If provided, prints extra debug information", action='store_true')
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-r', '--relevant', help="A file containing the relevant URLs")
    requiredNamed.add_argument('-n', '--nonrelevant', help="A file containing non-relevant URLs")
    requiredNamed.add_argument('-sw', '--stopwords', help="A file containing stop words")
    requiredNamed.add_argument('-mo', '--modelout', help="The file to store the generated model in")
    requiredNamed.add_argument('-vo', '--vectorout', help="The file to store the generated vectorizer in")
    args = parser.parse_args()
    
    # Checking if all required arguments were supplied
    if args.relevant is None or args.nonrelevant is None or args.stopwords is None or args.modelout is None or args.vectorout is None:
        print("Error! Not all required parameters were set!")
        parser.print_usage()
    else:
        # Grab the links from the files
        rel_fp = open(args.relevant, "r")
        rel = rel_fp.read().splitlines()
        rel_fp.close()
        
        notrel_fp = open(args.nonrelevant, "r")
        notrel = notrel_fp.read().splitlines()
        notrel_fp.close()
        
        # Scrape each URL in both collections
        print("Scraping articles")
        scrape_links(rel, True, verbose = args.verbose)
        scrape_links(notrel, False, verbose = args.verbose)
        
        # Normalize the extracted text
        print("Normalizing text")
        scraped["norm_text"] = scraped.content.apply(normalize_text)
        
        # Create a corpus from the normalized text
        print("Creating corpus")
        corpus = createCorpus(scraped)
        stop_words = [x.strip() for x in open(args.stopwords,'r').read().split('\n')]
        
        # Creating TFIDF vectors
        print("Creating TFIDF vectors")
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        K = vectorizer.fit_transform(corpus)
        
        # Splitting data into separate training and testing data
        X_train, X_test, y_train, y_test = train_test_split(K, bool_array, test_size = 0.2, random_state = 255)
        
        # Training RandomForestClassifier
        print("Training RandomForestClassifier")
        clf = RandomForestClassifier(max_depth=19, n_estimators = 7, max_features = "auto", min_samples_leaf = 1, random_state = 15, n_jobs = -1)
        clf.fit(X_train, y_train)
        
        # Testing RandomForestClassifier
        score_forest = clf.score(X_test, y_test)
        print("Classifier accuracy: %s" % score_forest)
        
        # Dumping the trained model and vectorizer to the specified files
        print("Dumping model and vectorizer")
        pickle.dump(clf, open(args.modelout, "wb"))
        pickle.dump(vectorizer, open(args.vectorout, "wb"))
