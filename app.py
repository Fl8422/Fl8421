from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = FastAPI()

# Настройка CORS для вашего GitHub Pages сайта
origins = [
    "https://ваш-username.github.io",
    "https://ваш-username.github.io/ваш-репозиторий",  # Замените на ваш фактический URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    """
    Маршрут для вкладки Parser. Выполняет поиск в Google и возвращает первые 10 ссылок.
    """
    driver = get_webdriver()
    try:
        driver.get('https://www.google.com')

        # Поиск
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(q)
        search_box.submit()

        time.sleep(2)  # Ждем загрузки страницы

        # Получение ссылок
        links = []
        search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        for result in search_results[:10]:  # Ограничимся первыми 10 результатами
            href = result.get_attribute('href')
            links.append(href)

        return {"links": links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.quit()

@app.get("/glaz-boga-search")
def glaz_boga_search(q: str = Query(..., min_length=1), types: str = Query(..., min_length=1)):
    """
    Маршрут для вкладки Глаз бога. Выполняет поиск по указанным типам: phone, telegram, vehicle.
    """
    types_list = types.split(',')
    results = {}

    # Поиск по номеру телефона
    if 'phone' in types_list:
        phone_results = {}
        phone_results.update(search_whitepages(q))
        phone_results.update(search_spokeo(q))
        phone_results.update(search_numberguru(q))
        phone_results.update(search_media_sova(q))
        phone_results.update(search_phone_radar(q))
        phone_results.update(search_getcontact(q))
        results['phone'] = phone_results

    # Поиск по Telegram аккаунту
    if 'telegram' in types_list:
        telegram_results = {}
        telegram_results.update(search_tgstat(q))
        telegram_results.update(search_telegram_directory(q))
        telegram_results.update(search_telemetr(q))
        telegram_results.update(search_combot(q))
        telegram_results.update(search_tgstat_ru(q))
        telegram_results.update(search_telegraph(q))
        telegram_results.update(search_tlgrm_ru(q))
        telegram_results.update(search_telegram_analytics(q))
        telegram_results.update(search_tgstat_com(q))
        telegram_results.update(search_telegraph_directory(q))
        results['telegram'] = telegram_results

    # Поиск по номеру автомобиля
    if 'vehicle' in types_list:
        vehicle_results = {}
        vehicle_results.update(search_ukr_zone(q))
        vehicle_results.update(search_unda_com_ua(q))
        vehicle_results.update(search_opendatabot_ua(q))
        vehicle_results.update(search_carsua_net(q))
        results['vehicle'] = vehicle_results

    return {"results": results}

# Запуск приложения можно осуществить с помощью Uvicorn
# Например, командой: uvicorn app:app --host 0.0.0.0 --port 8000
