import requests

API_KEY = "AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw"
CSE_ID = "1277afbc49d06402d"

def perform_search(query, search_type):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
    }

    if search_type == "Поиск по времени":
        params["sort"] = "date:r:now-7d"
    elif search_type == "Поиск по сайту":
        params["q"] = f"site:{query}"

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        return [item["link"] for item in data.get("items", [])]
    except Exception as e:
        return [f"Ошибка: {str(e)}"]
