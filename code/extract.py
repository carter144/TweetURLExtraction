#!/usr/bin/env python3

# Importing relevant Python libraries
import pandas
import requests
from queue import Queue
from threading import Thread
import argparse

# Resolves a shortened URL to its final form
def resolve_url(url):
    try:
        response = requests.head(url, allow_redirects = True, verify = False, timeout = 10)
    except Exception:
        return None
    return response.url

# Wrapper for multithreaded resolution
def work(q, resolved):
    while True:
        url = q.get()
        resolved[url] = resolve_url(url)
        q.task_done()

# Expands a list of shortened URLs to the final URLs
def resolve_urls(urls, n_threads = 5):
    resolved = {}
    
    urls = list(set(urls)) # Remove duplicate URLs
    q = Queue(maxsize=0)
    for url in urls:
        q.put(url)

    for i in range(n_threads):
      worker = Thread(target=work, args=(q, resolved))
      worker.setDaemon(True)
      worker.start()
    
    q.join()
    
    return resolved

# Runs if invoked directly from the command line
if __name__ == "__main__":
    # Defining arguments to parse for
    parser = argparse.ArgumentParser(description='Extracts and resolves URLs within a Tweet collection')
    parser.add_argument('-eo', '--extendedoutput', help="The file to store the results and additional metadata in.")
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-t', '--tweetcollection', help="A JSON file containing the list of Tweets to process (exported from yourTwapperKeeper)")
    requiredNamed.add_argument('-o', '--output', help="The file to store a list of resolved URLs in.")
    
    args = parser.parse_args()
    
    if args.tweetcollection is None or args.output is None:
        print("Error! Not all required parameters were set!")
        parser.print_usage()
    else:
        # Loading the Tweet data
        print("Loading Tweets")
        tweet_df = pandas.read_json(args.tweetcollection)
        
        # Extracting the URLs from the DataFrame
        print("Extracting URLs from the Tweet collection")
        extracted_urls = []
        for idx, tweet in tweet_df.iterrows():
            tweet_id = tweet["id"]
            created_at = tweet.created_at
            user_screen_name = tweet.user["screen_name"]
            tweet_url = "https://twitter.com/%s/status/%d" % (user_screen_name, tweet_id)
            for url in tweet.entities["urls"]:
                extracted_urls.append([tweet_id, tweet_url, created_at, url["expanded_url"]])
        
        # Creating a new dataframe from the extracted URLs
        url_df = pandas.DataFrame(extracted_urls, columns = ["tweet_id", "tweet_url", "created_at", "url"])
        
        # Suppressing InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        
        # Resolving the URLs within the dataframe
        print("Resolving shortened URLs")
        resolved = resolve_urls(url_df.url, n_threads = 5)
        url_df["resolved"] = url_df.url.apply(lambda X: resolved[X])
        
        # Saving output to a file
        print("Saving results")
        out_f = open(args.output, 'w')
        for resolved in url_df.resolved:
            out_f.write("%s\n" % resolved)
        out_f.close()
            
        if args.extendedoutput is not None:
            url_df.to_csv(args.extendedoutput, index = False)
