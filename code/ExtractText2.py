
# coding: utf-8

# In[28]:


# Importing necessary libraries
import pandas
import newspaper
import re
import simhash


# In[2]:


# Reading in the extracted content
extracted = pandas.read_csv("../data/url_info.csv", encoding = "iso8859")
extracted.head()


# In[3]:


# Function to extract the text from the html of each article
def convert_text(html):
    try:
        return newspaper.fulltext(html)
    except:
        return ""


# In[4]:


extracted["text"] = extracted.content.apply(convert_text)


# In[5]:


extracted.head()


# In[20]:


space_re = re.compile("[\s]{2,}")
char_re = re.compile("([A-Za-z0-9]+)[^A-Za-z0-9\s]+([A-Za-z0-9]+)")
right_re = re.compile("([A-Za-z0-9]+)[^A-Za-z0-9\s]+")
left_re = re.compile("[^A-Za-z0-9\s]+([A-Za-z0-9]+)")
center_re = re.compile("\s*[^A-Za-z0-9\s]+\s*")
url_re = re.compile("https{0,1}://[^\s]+")
url2_re = re.compile("[a-z0-9\.]+\.[a-z0-9\.]+/[^\s]*")

def normalize_text(text):
    # Converting text to lowercase
    text = text.lower()
    
    # Removing URLs
    text = url_re.sub(" ", text)
    text = url2_re.sub(" ", text)
    
    # Removing non-alphanumeric characters
    text = char_re.sub("\g<1>\g<2>", text)
    text = right_re.sub("\g<1>", text)
    text = left_re.sub("\g<1>", text)  
    text = center_re.sub(" ", text)
    
    # Removing multiple spacing characters
    text = space_re.sub(" ", text)
    
    # Stripping leading and trailing spaces
    text = text.strip()
    
    return text


# In[21]:


extracted["norm_text"] = extracted.text.apply(normalize_text)


# In[22]:


extracted.head()


# In[25]:


extracted.iloc[48].norm_text


# In[29]:


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


# In[30]:


extracted.content_hash = extracted.norm_text.apply(lambda X: simhash.Simhash(get_features(X)).value)
extracted.head()

