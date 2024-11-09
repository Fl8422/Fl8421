import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Замените API_KEY и CX на ваши значения
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
SEARCH_ENGINE_ID = 'YOUR_SEARCH_ENGINE_ID'
GOOGLE_CUSTOM_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

def google_search(query):
    params = {
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query
    }
    response = requests.get(GOOGLE_CUSTOM_SEARCH_URL, params=params)
    results = response.json().get('items', [])
    links = [item['link'] for item in results]
    return links

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Нет поискового запроса'}), 400

    links = google_search(query)
    return jsonify({'links': links})

if __name__ == '__main__':
    app.run(port=5326)
