# seo_panel/seo_search.py
from googlesearch import search

def https://www.google.com/(query, num_results=10):
    results = []
    for url in search(query, num=num_results, stop=num_results, pause=2):
        results.append(url)
    return results
