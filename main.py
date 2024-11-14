import telebot
from flask import Flask, request, jsonify, render_template
import threading
import requests
import time

# Конфигурация
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
CSE_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
PASSWORD = "derts8524"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

# Хранение авторизованных пользователей
authorized_users = set()

# Функция для выполнения поиска через Google Custom Search API
def google_search(query, num_results=5, extract_text=False, search_type=""):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results,
    }

    if search_type == "image":
        params["searchType"] = "image"

    response = requests.get(search_url, params=params)
    time.sleep(2)  # Пауза между запросами

    if response.status_code == 200:
        results = response.json().get("items", [])
        search_results = []

        for item in results:
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet") if extract_text else ""

            if extract_text:
                search_results.append(f"<b>{title}</b>\n{snippet}\n<a href='{link}'>Ссылка</a>")
            else:
                search_results.append(f"<a href='{link}'>{link}</a>")

        return search_results
    else:
        return [f"Ошибка: не удалось выполнить запрос к Google API. Код состояния: {response.status_code}"]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in authorized_users:
        bot.send_message(message.chat.id, "Вы уже авторизованы.")
        send_main_menu(message)
    else:
        bot.send_message(message.chat.id, "Введите пароль для доступа:")

# Обработчик ввода пароля
@bot.message_handler(func=lambda message: message.text != "/start")
def password_handler(message):
    if message.text == PASSWORD:
        authorized_users.add(message.chat.id)
        bot.send_message(message.chat.id, "Пароль верный! Добро пожаловать.")
        send_main_menu(message)
    else:
        bot.send_message(message.chat.id, "Неверный пароль. Попробуйте еще раз.")

# Функция отправки главного меню
def send_main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    search_button = telebot.types.KeyboardButton("Поиск 🔍")
    detailed_search_button = telebot.types.KeyboardButton("Подробный поиск 📄")
    image_search_button = telebot.types.KeyboardButton("Поиск изображений 🖼️")
    time_filter_search_button = telebot.types.KeyboardButton("Поиск по дате 🕒")
    site_specific_search_button = telebot.types.KeyboardButton("Поиск по сайту 🌐")
    web_app_button = telebot.types.InlineKeyboardButton("Открыть веб-приложение 🌐", url="https://your-web-app-url.com")
    markup.row(search_button, detailed_search_button)
    markup.row(image_search_button, time_filter_search_button)
    markup.row(site_specific_search_button, web_app_button)
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=markup)

# Обработчики различных типов поиска
@bot.message_handler(func=lambda message: message.text == "Поиск 🔍" and message.chat.id in authorized_users)
def search_request(message):
    bot.send_message(message.chat.id, "Напишите запрос для стандартного поиска:")
    bot.register_next_step_handler(message, search_query)

@bot.message_handler(func=lambda message: message.text == "Подробный поиск 📄" and message.chat.id in authorized_users)
def detailed_search_request(message):
    bot.send_message(message.chat.id, "Напишите запрос для подробного поиска:")
    bot.register_next_step_handler(message, detailed_search_query)

@bot.message_handler(func=lambda message: message.text == "Поиск изображений 🖼️" and message.chat.id in authorized_users)
def image_search_request(message):
    bot.send_message(message.chat.id, "Напишите запрос для поиска изображений:")
    bot.register_next_step_handler(message, image_search_query)

@bot.message_handler(func=lambda message: message.text == "Поиск по дате 🕒" and message.chat.id in authorized_users)
def time_filtered_search_request(message):
    bot.send_message(message.chat.id, "Напишите запрос для поиска с фильтром по дате (неделя):")
    bot.register_next_step_handler(message, time_filtered_search_query)

@bot.message_handler(func=lambda message: message.text == "Поиск по сайту 🌐" and message.chat.id in authorized_users)
def site_specific_search_request(message):
    bot.send_message(message.chat.id, "Напишите запрос и укажите сайт (например, 'ноутбук site:example.com'):")
    bot.register_next_step_handler(message, site_specific_search_query)

# Функции обработки запросов для каждого типа поиска
def search_query(message):
    query = message.text
    bot.send_message(message.chat.id, "Поиск...")
    try:
        links = google_search(query, num_results=10, extract_text=False)
        response = "Результаты поиска:\n\n" + "\n\n".join(links)
        bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при поиске: {str(e)}")

def detailed_search_query(message):
    query = message.text
    bot.send_message(message.chat.id, "Подробный поиск...")
    try:
        results = google_search(query, num_results=5, extract_text=True)
        response = "Результаты подробного поиска:\n\n" + "\n\n".join(results)
        bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при подробном поиске: {str(e)}")

def image_search_query(message):
    query = message.text
    bot.send_message(message.chat.id, "Поиск изображений...")
    try:
        links = google_search(query, num_results=5, extract_text=False, search_type="image")
        response = "Результаты поиска изображений:\n\n" + "\n\n".join(links)
        bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при поиске изображений: {str(e)}")

def time_filtered_search_query(message):
    query = message.text
    bot.send_message(message.chat.id, "Поиск с фильтром по дате...")
    try:
        results = google_search(query + " after:7d", num_results=5, extract_text=False)
        response = "Результаты поиска по дате:\n\n" + "\n\n".join(results)
        bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при поиске по дате: {str(e)}")

def site_specific_search_query(message):
    query = message.text
    if 'site:' in query:
        bot.send_message(message.chat.id, "Поиск по сайту...")
        try:
            links = google_search(query, num_results=5, extract_text=True)
            response = "Результаты поиска по сайту:\n\n" + "\n\n".join(links)
            bot.send_message(message.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при поиске по сайту: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Введите запрос с форматом 'запрос site:example.com'.")

# Flask маршруты для веб-приложения
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def web_search():
    data = request.json
    query = data.get('query', '')
    search_type = data.get('search_type', 'standard')
    
    if search_type == "standard":
        results = google_search(query, num_results=10, extract_text=False)
    elif search_type == "detailed":
        results = google_search(query, num_results=5, extract_text=True)
    elif search_type == "image":
        results = google_search(query, num_results=5, extract_text=False, search_type="image")
    elif search_type == "time":
        results = google_search(query + " after:7d", num_results=5, extract_text=False)
    elif search_type == "site":
        results = google_search(query, num_results=5, extract_text=True)
    else:
        results = ["Неизвестный тип поиска."]
    
    return jsonify({"results": results})

# Функция запуска бота
def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # Запуск Flask и бота в отдельных потоках
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=5057)
