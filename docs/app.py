from flask import Flask, request, jsonify
from googlesearch import search

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def google_search():
    data = request.get_json()
    query = data.get("query")
    
    if not query:
        return jsonify({"error": "Запрос не задан"}), 400
    
    results = [url for url in search(query, num_results=20)]  # Получаем до 20 ссылок
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5421)
