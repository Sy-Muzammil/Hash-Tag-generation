from multiprocessing.pool import ThreadPool
from time import time as timer
from urllib2 import urlopen

urls = ["http://www.google.com", "http://www.apple.com", "http://www.microsoft.com", "http://www.amazon.com", "http://www.facebook.com"]

def fetch_url(url):
    try:
        response = urlopen(url)
        return url, response.read(), None
    except Exception as e:
        return url, None, e

start = timer()
results = ThreadPool(20).imap_unordered(fetch_url, urls)
for url, html, error in results:
    if error is None:
        print("%r fetched in %ss" % (url, timer() - start))
    else:
        print("error fetching %r: %s" % (url, error))
print("Elapsed Time: %s" % (timer() - start,))
