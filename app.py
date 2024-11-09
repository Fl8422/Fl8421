from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Настройка Selenium WebDriver
def get_webdriver():
    options = Options()
    options.add_argument('--headless')  # Безголовый режим
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# Функции для поиска по номеру телефона
def search_whitepages(phone):
    driver = get_webdriver()
    try:
        driver.get('https://www.whitepages.com/')
        search_box = driver.find_element(By.NAME, 'person')
        search_box.send_keys(phone)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        name_elements = driver.find_elements(By.CSS_SELECTOR, 'a.person-name')
        names = [elem.text for elem in name_elements]
        return {"WhitePages": {"names": names}}
    except Exception as e:
        return {"WhitePages": {"error": str(e)}}
    finally:
        driver.quit()

def search_spokeo(phone):
    driver = get_webdriver()
    try:
        driver.get('https://www.spokeo.com/')
        search_box = driver.find_element(By.NAME, 'query')
        search_box.send_keys(phone)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        name_elements = driver.find_elements(By.CSS_SELECTOR, 'div.PersonName')
        names = [elem.text for elem in name_elements]
        return {"Spokeo": {"names": names}}
    except Exception as e:
        return {"Spokeo": {"error": str(e)}}
    finally:
        driver.quit()

def search_numberguru(phone):
    driver = get_webdriver()
    try:
        driver.get('https://www.numberguru.com/')
        search_box = driver.find_element(By.ID, 'phone')
        search_box.send_keys(phone)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        info_elements = driver.find_elements(By.CSS_SELECTOR, 'div.number-info')
        info = [elem.text for elem in info_elements]
        return {"NumberGuru": {"info": info}}
    except Exception as e:
        return {"NumberGuru": {"error": str(e)}}
    finally:
        driver.quit()

def search_media_sova(phone):
    driver = get_webdriver()
    try:
        driver.get('https://mediasova.com/')
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(phone)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        results = driver.find_elements(By.CSS_SELECTOR, 'div.result-item')
        data = [elem.text for elem in results]
        return {"MediaSova": {"results": data}}
    except Exception as e:
        return {"MediaSova": {"error": str(e)}}
    finally:
        driver.quit()

def search_phone_radar(phone):
    driver = get_webdriver()
    try:
        driver.get('https://www.phoneradar.com/')
        search_box = driver.find_element(By.NAME, 'phone')
        search_box.send_keys(phone)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        info_elements = driver.find_elements(By.CSS_SELECTOR, 'div.phone-info')
        info = [elem.text for elem in info_elements]
        return {"PhoneRadar": {"info": info}}
    except Exception as e:
        return {"PhoneRadar": {"error": str(e)}}
    finally:
        driver.quit()

def search_getcontact(phone):
    driver = get_webdriver()
    try:
        driver.get('https://getcontact.com/')
        search_box = driver.find_element(By.NAME, 'query')
        search_box.send_keys(phone)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        info_elements = driver.find_elements(By.CSS_SELECTOR, 'div.contact-info')
        info = [elem.text for elem in info_elements]
        return {"GetContact": {"info": info}}
    except Exception as e:
        return {"GetContact": {"error": str(e)}}
    finally:
        driver.quit()

# Функции для поиска по Telegram аккаунту
def search_tgstat(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://tgstat.ru/channel/{username}')
        time.sleep(3)
        # Пример извлечения данных
        title = driver.find_element(By.CSS_SELECTOR, 'h1.channel-title').text
        return {"TGStat": {"title": title}}
    except Exception as e:
        return {"TGStat": {"error": str(e)}}
    finally:
        driver.quit()

def search_telegram_directory(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://telegram-directory.com/{username}')
        time.sleep(3)
        # Пример извлечения данных
        info = driver.find_element(By.CSS_SELECTOR, 'div.user-info').text
        return {"TelegramDirectory": {"info": info}}
    except Exception as e:
        return {"TelegramDirectory": {"error": str(e)}}
    finally:
        driver.quit()

def search_telemetr(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://telemetr.me/channel/{username}')
        time.sleep(3)
        # Пример извлечения данных
        stats = driver.find_element(By.CSS_SELECTOR, 'div.stats').text
        return {"Telemetr": {"stats": stats}}
    except Exception as e:
        return {"Telemetr": {"error": str(e)}}
    finally:
        driver.quit()

def search_combot(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://combot.org/telegram/{username}')
        time.sleep(3)
        # Пример извлечения данных
        info = driver.find_element(By.CSS_SELECTOR, 'div.profile-info').text
        return {"Combot": {"info": info}}
    except Exception as e:
        return {"Combot": {"error": str(e)}}
    finally:
        driver.quit()

def search_tgstat_ru(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://tgstat.ru/channel/{username}')
        time.sleep(3)
        # Пример извлечения данных
        title = driver.find_element(By.CSS_SELECTOR, 'h1.channel-title').text
        return {"Tgstat.ru": {"title": title}}
    except Exception as e:
        return {"Tgstat.ru": {"error": str(e)}}
    finally:
        driver.quit()

def search_telegraph(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://telegra.ph/{username}')
        time.sleep(3)
        # Пример извлечения данных
        content = driver.find_element(By.CSS_SELECTOR, 'div.content').text
        return {"Telegraph": {"content": content}}
    except Exception as e:
        return {"Telegraph": {"error": str(e)}}
    finally:
        driver.quit()

def search_tlgrm_ru(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://tlgrm.ru/{username}')
        time.sleep(3)
        # Пример извлечения данных
        info = driver.find_element(By.CSS_SELECTOR, 'div.user-info').text
        return {"TLGRM.ru": {"info": info}}
    except Exception as e:
        return {"TLGRM.ru": {"error": str(e)}}
    finally:
        driver.quit()

def search_telegram_analytics(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://telegram-analytics.com/{username}')
        time.sleep(3)
        # Пример извлечения данных
        stats = driver.find_element(By.CSS_SELECTOR, 'div.analytics-stats').text
        return {"TelegramAnalytics": {"stats": stats}}
    except Exception as e:
        return {"TelegramAnalytics": {"error": str(e)}}
    finally:
        driver.quit()

def search_tgstat_com(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://tgstat.com/channel/{username}')
        time.sleep(3)
        # Пример извлечения данных
        stats = driver.find_element(By.CSS_SELECTOR, 'div.channel-stats').text
        return {"Tgstat.com": {"stats": stats}}
    except Exception as e:
        return {"Tgstat.com": {"error": str(e)}}
    finally:
        driver.quit()

def search_telegraph_directory(username):
    driver = get_webdriver()
    try:
        driver.get(f'https://telegraph-directory.com/{username}')
        time.sleep(3)
        # Пример извлечения данных
        info = driver.find_element(By.CSS_SELECTOR, 'div.profile-details').text
        return {"TelegraphDirectory": {"info": info}}
    except Exception as e:
        return {"TelegraphDirectory": {"error": str(e)}}
    finally:
        driver.quit()

# Функции для поиска по номеру автомобиля
def search_ukr_zone(vehicle_number):
    driver = get_webdriver()
    try:
        driver.get('https://ukr.zone/')
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(vehicle_number)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        owner = driver.find_element(By.CSS_SELECTOR, 'div.owner-info').text
        return {"ukr.zone": {"owner": owner}}
    except Exception as e:
        return {"ukr.zone": {"error": str(e)}}
    finally:
        driver.quit()

def search_unda_com_ua(vehicle_number):
    driver = get_webdriver()
    try:
        driver.get('https://unda.com.ua/')
        search_box = driver.find_element(By.NAME, 'query')
        search_box.send_keys(vehicle_number)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        owner = driver.find_element(By.CSS_SELECTOR, 'div.owner-details').text
        return {"unda.com.ua": {"owner": owner}}
    except Exception as e:
        return {"unda.com.ua": {"error": str(e)}}
    finally:
        driver.quit()

def search_opendatabot_ua(vehicle_number):
    driver = get_webdriver()
    try:
        driver.get('https://opendatabot.ua/')
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(vehicle_number)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        details = driver.find_element(By.CSS_SELECTOR, 'div.vehicle-details').text
        return {"opendatabot.ua": {"details": details}}
    except Exception as e:
        return {"opendatabot.ua": {"error": str(e)}}
    finally:
        driver.quit()

def search_carsua_net(vehicle_number):
    driver = get_webdriver()
    try:
        driver.get('https://carsua.net/')
        search_box = driver.find_element(By.NAME, 'search')
        search_box.send_keys(vehicle_number)
        search_box.submit()
        time.sleep(3)
        # Пример извлечения данных
        owner = driver.find_element(By.CSS_SELECTOR, 'div.owner-info').text
        return {"carsua.net": {"owner": owner}}
    except Exception as e:
        return {"carsua.net": {"error": str(e)}}
    finally:
        driver.quit()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Пример реализации первой вкладки Parser (Google поиск)
    driver = get_webdriver()
    try:
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

        return jsonify({"links": links})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

@app.route('/glaz-boga-search', methods=['GET'])
def glaz_boga_search():
    query = request.args.get('q')
    types = request.args.get('types')  # Формат: 'phone,telegram,vehicle'
    if not query or not types:
        return jsonify({"error": "Missing query or types"}), 400

    types = types.split(',')

    results = {}

    # Поиск по номеру телефона
    if 'phone' in types:
        phone_results = {}
        phone_results.update(search_whitepages(query))
        phone_results.update(search_spokeo(query))
        phone_results.update(search_numberguru(query))
        phone_results.update(search_media_sova(query))
        phone_results.update(search_phone_radar(query))
        phone_results.update(search_getcontact(query))
        results['phone'] = phone_results

    # Поиск по Telegram аккаунту
    if 'telegram' in types:
        telegram_results = {}
        telegram_results.update(search_tgstat(query))
        telegram_results.update(search_telegram_directory(query))
        telegram_results.update(search_telemetr(query))
        telegram_results.update(search_combot(query))
        telegram_results.update(search_tgstat_ru(query))
        telegram_results.update(search_telegraph(query))
        telegram_results.update(search_tlgrm_ru(query))
        telegram_results.update(search_telegram_analytics(query))
        telegram_results.update(search_tgstat_com(query))
        telegram_results.update(search_telegraph_directory(query))
        results['telegram'] = telegram_results

    # Поиск по номеру автомобиля
    if 'vehicle' in types:
        vehicle_results = {}
        vehicle_results.update(search_ukr_zone(query))
        vehicle_results.update(search_unda_com_ua(query))
        vehicle_results.update(search_opendatabot_ua(query))
        vehicle_results.update(search_carsua_net(query))
        results['vehicle'] = vehicle_results

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()
