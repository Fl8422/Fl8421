from flask import Flask, request, jsonify
from googlesearch import search

app = Flask(__name__)

@app.route('/search')
def google_search():
    query = request.args.get('q')
    num_results = 10  # или можете изменить количество ссылок от 3 до 20
    results = []
    for url in search(query, num=num_results, stop=num_results, pause=2):
        results.append(url)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(port:5422)
