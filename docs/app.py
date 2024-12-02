import json
from googleapiclient.discovery import build
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw"
CX = "1277afbc49d06402d"

def google_search(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CX).execute()
    return res['items'] if 'items' in res else []

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    if request.method == "POST":
        query = request.form.get("query")
        search_results = google_search(query)
    return render_template("index.html", search_results=search_results)

if __name__ == "__main__":
    app.run(port=5749)
