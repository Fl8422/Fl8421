from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Настройка Selenium
    options = Options()
    options.add_argument('--headless')  # Безголовый режим
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com')

    # Поиск
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.submit()

    time.sleep(2)  # Ждем загрузки страницы

    # Получение ссылок
    links = []
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
    for result in search_results[:10]:  # Ограничимся первыми 10 результатами
        href = result.get_attribute('href')
        links.append(href)

    driver.quit()

    return jsonify({"links": links})

if __name__ == '__main__':
    app.run()
