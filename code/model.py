from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import sys
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from pprint import pprint

bool_array = []
def createCorpus(csvFile):
	corpus_array = []
	
	with open(csvFile, "r", encoding="utf8") as f:
		reader = csv.reader(f)
		# trues = 0
		# falses = 0
		for row in reader:
			corpus_array.append(row[4])
			if row[1].lower() == "false" or row[2] != "200" or len(row[4]) == 0:
				bool_array.append(0)
				# falses = falses + 1
			else:
				bool_array.append(1)
				# trues = trues + 1
	# print("True count is: " + str(trues))
	# print("false count is: " + str(falses))

	return corpus_array


# Training
corpus = createCorpus("../data/url_info.csv")
stop_words = [x.strip() for x in open('../data/stop_words.txt','r').read().split('\n')]
vectorizer = TfidfVectorizer(stop_words=stop_words)

y = np.array(bool_array)[0:2000]

K = vectorizer.fit_transform(corpus)
X = K[0:2000]
	
clf = RandomForestClassifier(max_depth=10, random_state=0)
clf.fit(X, y)


# Testing
y2 = np.array(bool_array)[2000:]
X2 = K[2000:]
print(clf.score(X2, y2))