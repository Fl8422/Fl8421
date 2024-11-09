from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов. Можно настроить более строго.

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    count = int(request.args.get('count', 10))  # Количество результатов (по умолчанию 10)
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Безголовый режим
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    try:
        # Используем webdriver-manager для автоматической установки ChromeDriver
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    except Exception as e:
        return jsonify({"error": f"Ошибка инициализации браузера: {str(e)}"}), 500

    try:
        driver.get('https://www.google.com')

        # Принять соглашение, если отображается
        try:
            agree_button = driver.find_element(By.XPATH, "//div[contains(text(),'I agree')]")
            agree_button.click()
            time.sleep(1)
        except:
            pass  # Если кнопка не найдена, продолжаем

        # Поиск
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.submit()

        time.sleep(2)  # Ждем загрузки страницы

        # Получение ссылок
        links = []
        search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        for result in search_results[:count]:  # Ограничимся первыми 'count' результатами
            href = result.get_attribute('href')
            links.append(href)

    except Exception as e:
        return jsonify({"error": f"Ошибка при поиске: {str(e)}"}), 500
    finally:
        driver.quit()

    return jsonify({"links": links})

if __name__ == '__main__':
    app.run()
