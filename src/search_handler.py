import requests
from config import GOOGLE_API_KEY

def perform_search(query, search_type):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "q": query, "cx": "your_cx_id"}  # Замените на ваш cx ID

    if search_type == "Подробный":
        params["fields"] = "items(title, link, snippet)"
    elif search_type == "По времени":
        params["dateRestrict"] = "w[1]"
    elif search_type == "По сайту":
        site = query.split("site:")[-1].strip()
        params["q"] = f"site:{site}"

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [f"{item['title']}: {item['link']}" for item in data.get("items", [])]
    else:
        return ["Ошибка запроса! Проверьте API ключ."]
