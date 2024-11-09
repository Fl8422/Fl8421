from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

app = Flask(__name__)

GOOGLE_SEARCH_URL = "https://www.google.com/search"

def google_search(query):
    params = {'q': query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(GOOGLE_SEARCH_URL, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for item in soup.find_all('a'):
        href = item.get('href')
        if href and '/url?q=' in href:
            url = href.split('/url?q=')[1].split('&')[0]
            links.append(url)
    return links

def parse_website(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Здесь добавьте логику парсинга нужной информации
        title = soup.title.string if soup.title else 'Без заголовка'
        return {'url': url, 'title': title}
    except Exception as e:
        return {'url': url, 'error': str(e)}

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Нет поискового запроса'}), 400

    links = google_search(query)
    parsed_links = [parse_website(link) for link in links[:10]]  # Парсим первые 10 результатов
    return jsonify({'links': [link['url'] for link in parsed_links]})

if __name__ == '__main__':
    app.run(port=5326)
