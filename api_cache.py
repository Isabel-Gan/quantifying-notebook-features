import pylru

global api_cache

def init_cache():
    global api_cache
    api_cache = pylru.lrucache(20)

def add_to_cache(url, response):
    global api_cache
    api_cache[url] = response

def is_in_cache(url):
    global api_cache 
    if url in api_cache:
        return api_cache[url]
    else:
        return None