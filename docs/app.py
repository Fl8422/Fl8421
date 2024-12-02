from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Замените этот ключ на свой API ключ Google
GOOGLE_API_KEY = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw'
CX = '1277afbc49d06402d'

def search_google(query, search_type):
    search_url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CX}'
    
    # Параметры поиска по времени или сайту
    if search_type == 'time':
        search_url += '&dateRestrict=w1'  # Для поиска по времени за неделю
    elif search_type == 'site':
        search_url += f'&siteSearch={query}'
    
    response = requests.get(search_url)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    search_type = request.args.get('type', 'standard')

    search_results = search_google(query, search_type)
    
    results = []
    if 'items' in search_results:
        for item in search_results['items']:
            results.append({
                'title': item['title'],
                'link': item['link'],
                'snippet': item.get('snippet', '')
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
