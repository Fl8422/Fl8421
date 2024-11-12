# seo_panel/site_specific_search.py
import requests
from bs4 import BeautifulSoup

def https://www.google.com/(site_url, keyword):
    results = []
    response = requests.get(site_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            if keyword.lower() in link.text.lower():
                results.append(link['href'])
    return results
