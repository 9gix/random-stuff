import time
import requests

def reqmark(url):
    """return the time(second) for making a url request""" 
    start = time.time()
    r = requests.get(url)
    duration = time.time() - start
    if r.status_code != 200:
        print r.status_code
    return duration



