from flask import Flask, render_template, request
from googleapiclient.discovery import build
import os
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Замените на ваши ключ и ID поисковой системы
API_KEY = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw'
SEARCH_ENGINE_ID = '1277afbc49d06402d'

service = build("customsearch", "v1", developerKey=API_KEY)

def perform_search(query, search_type, site=None, time_period=None):
    params = {
        'q': query,
        'cx': SEARCH_ENGINE_ID,
        'num': 20
    }

    if search_type == 'standard':
        pass  # Стандартный поиск
    elif search_type == 'detailed':
        pass  # Подробный поиск с извлечением текста
    elif search_type == 'standard_time':
        params['dateRestrict'] = 'w1'  # За последнюю неделю
    elif search_type == 'detailed_time':
        params['dateRestrict'] = 'w1'
    elif search_type == 'site':
        params['q'] += f' site:{site}'
    elif search_type == 'image':
        params['searchType'] = 'image'

    try:
        response = service.cse().list(**params).execute()
        items = response.get('items', [])
        results = []

        for item in items:
            if search_type in ['detailed', 'detailed_time', 'site']:
                # Извлечение текста из анкеты
                page = requests.get(item['link'])
                soup = BeautifulSoup(page.content, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                results.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': text[:200]  # Ограничение текста
                })
            else:
                results.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': item.get('snippet')
                })
        return results
    except Exception as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    query = ''
    if request.method == 'POST':
        query = request.form.get('query')
        search_type = request.form.get('search_type')
        site = request.form.get('site') if search_type == 'site' else None
        results = perform_search(query, search_type, site=site)
    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    # Для локальной разработки
    app.run(host='0.0.0.0', port=5842, debug=True)
