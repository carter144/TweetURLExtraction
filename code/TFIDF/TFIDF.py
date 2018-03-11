#Term Frequency(TF) : number of times a word appears in a document. 
#Inverse Document Frequency (IDF) : logarithm of (number of the documents in the corpus) / (number of documents where the specific term appears)  

# tf-idf weight: Term Frequency(TF)/Inverse Document Frequency 


documents = [] #global documents list
keyword = None #keyword 
termFrequency = 0

def init():
	keyword_file = open("keyword.txt", "r")
	global keyword
	keyword = keyword_file.read() + ""

	news_file = open("news5.txt", "r") #open first news file
	documents.append(news_file.read()) #append to global documents list
	return;



def tf():
	document = documents[0]
	for word in document.split():
		global termFrequency
		if word.lower() in keyword.lower():
			termFrequency += 1
	return;

init() #reads news files and keyword file
tf()
print termFrequency

#5 articles
#load documents
#corpus 1
#corpus 2
#corpus 3 
