import telebot
from telebot import types
import time
import threading
import random

# Вставьте ваш токен бота здесь
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_TELEGRAM_ID = 6400017164  # Замените на ваш ID

# Словарь для хранения данных пользователей
user_data = {}
user_data_lock = threading.Lock()  # Блокировка для синхронизации доступа к user_data

# Геймпассы
game_passes = {
    'double_luck': {
        'name': 'Удвоение Удачи',
        'price': 750000,
        'effect': 'double_luck',
        'description': 'Удваивает удачу при добыче руды.',
    },
    'ultra_luck': {
        'name': 'Ультра Удача',
        'price': 2500000,
        'effect': 'ultra_luck',
        'description': 'Увеличивает удачу при добыче руды в 5 раз.',
    },
    'double_ore': {
        'name': 'Двойная Руда',
        'price': 1000000,
        'effect': 'double_ore',
        'description': 'Удваивает количество добытой руды при добыче.',
    },
    'instant_smelting': {
        'name': 'Моментальная Переплавка',
        'price': 1500000,
        'effect': 'instant_smelting',
        'description': 'Позволяет переплавлять руду без ожидания 3 секунд.',
    }
}

# Майнеры (10 уникальных)
miners = [
    {'name': 'Майнер Начинающий', 'price': 7500, 'earn_per_10_hours': 200},
    {'name': 'Майнер Продвинутый', 'price': 15000, 'earn_per_10_hours': 500},
    {'name': 'Майнер Эксперт', 'price': 22500, 'earn_per_10_hours': 700},
    {'name': 'Майнер Мастер', 'price': 30000, 'earn_per_10_hours': 1100},
    {'name': 'Майнер Профи', 'price': 37500, 'earn_per_10_hours': 1500},
    {'name': 'Майнер Гуру', 'price': 45000, 'earn_per_10_hours': 1800},
    {'name': 'Майнер Легенда', 'price': 52500, 'earn_per_10_hours': 2200},
    {'name': 'Майнер Великий', 'price': 60000, 'earn_per_10_hours': 2500},
    {'name': 'Майнер Император', 'price': 67500, 'earn_per_10_hours': 3000},
    {'name': 'Майнер Бессмертный', 'price': 75000, 'earn_per_10_hours': 3500},
]

# Руды для каждой планеты с увеличенным количеством
ores = {
    'Earth': [
        {'name': 'Камень', 'weight': 50},
        {'name': 'Уголь', 'weight': 40},
        {'name': 'Железная руда', 'weight': 30},
        {'name': 'Медная руда', 'weight': 25},
        {'name': 'Золотая руда', 'weight': 20},
        {'name': 'Серебряная руда', 'weight': 15},
        {'name': 'Алмазная руда', 'weight': 10},
        {'name': 'Платиновая руда', 'weight': 5},
        {'name': 'Редкая руда', 'weight': 3},
        {'name': 'Легендарная руда', 'weight': 1},
        # Дополнительные руды
        {'name': 'Титан', 'weight': 2},
        {'name': 'Никель', 'weight': 4},
        {'name': 'Палладий', 'weight': 2},
        {'name': 'Родий', 'weight': 1},
        {'name': 'Селен', 'weight': 3}
    ],
    'Moon': [
        {'name': 'Лунный Камень', 'weight': 20},
        {'name': 'Реголит', 'weight': 15},
        {'name': 'Титанит', 'weight': 10},
        {'name': 'Силикат', 'weight': 5},
        {'name': 'Гранат', 'weight': 2}
    ],
    'Mars': [
        {'name': 'Феолит', 'weight': 20},
        {'name': 'Марганец', 'weight': 15},
        {'name': 'Хром', 'weight': 10},
        {'name': 'Кобальт', 'weight': 5},
        {'name': 'Ванадий', 'weight': 2}
    ]
}

# Характеристики кирок, рюкзаков, печей и шахт (опущены для краткости)
# ...

# Ребирты (опущены для краткости)
rebirths = [
    {'name': 'Новичёк', 'price': 100000},
    {'name': 'Опытный', 'price': 200000},
    {'name': 'Профессионал', 'price': 300000},
    {'name': 'Мастер', 'price': 400000},
    {'name': 'Гуру', 'price': 500000},
    {'name': 'Эксперт', 'price': 600000},
    {'name': 'Легенда', 'price': 700000},
    {'name': 'Великий', 'price': 800000},
    {'name': 'Император', 'price': 900000},
    {'name': 'Бессмертный', 'price': 1000000}
]

# Команда /start
@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    with user_data_lock:
        if user_id not in user_data:
            user_data[user_id] = {
                'current_planet': 'Earth',  # Начальная планета: Земля
                'purchased_planets': ['Earth'],  # Игрок начинает только с Земли
                'pickaxe_level': {'Earth': 1},
                'backpack_level': {'Earth': 1},
                'furnace_level': {'Earth': 1},
                'mine_level': {'Earth': 1},
                'balance': 0,  # Начальный баланс установлен в 0 монет
                'ores': {'Earth': {}, 'Moon': {}, 'Mars': {}},
                'smelting': {'Earth': {}, 'Moon': {}, 'Mars': {}},
                'coal': {'Earth': 0, 'Moon': 0, 'Mars': 0},
                'is_mining': {'Earth': False, 'Moon': False, 'Mars': False},
                'purchased_pickaxes': {'Earth': [1], 'Moon': [], 'Mars': []},  # Список купленных кирок
                'purchased_backpacks': {'Earth': [1], 'Moon': [], 'Mars': []},  # Список купленных рюкзаков
                'purchased_furnaces': {'Earth': [1], 'Moon': [], 'Mars': []},  # Список купленных печей
                'purchased_mines': {'Earth': [1], 'Moon': [], 'Mars': []},  # Список купленных шахт
                'ingots': {'Earth': {}, 'Moon': {}, 'Mars': {}},
                'rebirth_count': 0,  # Количество ребиртов
                'multiplier': 1,  # Множитель монет
                'game_passes': {},  # Список приобретённых геймпассов
                'clicker': {
                    'enabled': False,
                    'last_click_time': 0
                },
                'miners_owned': []
            }
    welcome_text = (
        "Добро пожаловать в игру *Шахтёр*!\n\n"
        "Вы начинаете своё путешествие на планете *Земля*.\n"
        "Исследуйте рудные поля, улучшайте своё оборудование и открывайте новые планеты для ещё больших возможностей!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')
    show_main_menu(message)

# Функция для отображения главного меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mine_button = types.KeyboardButton('⛏ Добывать руду')
    furnace_button = types.KeyboardButton('🔥 Печь')
    sell_button = types.KeyboardButton('💰 Продать руду')
    shop_button = types.KeyboardButton('🛒 Магазин')
    balance_button = types.KeyboardButton('💎 Баланс')
    inventory_button = types.KeyboardButton('🎒 Мой портфель')
    switch_planet_button = types.KeyboardButton('🔄 Переключиться на планету')  # Новая кнопка для переключения планет
    help_button = types.KeyboardButton('❓ Помощь')
    user_id = message.from_user.id
    with user_data_lock:
        if user_id == ADMIN_TELEGRAM_ID:
            admin_button = types.KeyboardButton('🔴 Админ панель 🔴')
            markup.add(admin_button)
    markup.add(mine_button, furnace_button)
    markup.add(sell_button, shop_button)
    markup.add(balance_button, inventory_button)
    markup.add(switch_planet_button)
    markup.add(help_button)
    bot.send_message(message.chat.id, "Главное меню", reply_markup=markup)

# Обработчик для раздела "Помощь"
@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
def show_help(message):
    faq_text = """
*Часто задаваемые вопросы (FAQ):*

1️⃣ *Как начать игру?*
- Используйте команду /start, чтобы начать игру и инициализировать ваш профиль.

2️⃣ *Как добывать руду?*
- В главном меню нажмите на кнопку ⛏ Добывать руду. Каждая добыча занимает 3 секунды.
- Чем выше уровень вашей *кирки*, тем более ценные руды вы сможете добывать.
- Чем выше уровень вашей *шахты*, тем больше шанс найти редкие и ценные руды.

3️⃣ *Как переплавлять руду?*
- В главном меню выберите 🔥 Печь, затем добавьте уголь и переплавьте руду.
- Чем выше уровень вашей *печи*, тем больше руды можно переплавить за раз.

4️⃣ *Как продавать руду?*
- Нажмите на 💰 Продать руду в главном меню, чтобы продать все переплавленные руды.

5️⃣ *Как улучшить оборудование?*
- Воспользуйтесь 🛒 Магазин для покупки новых кирок, рюкзаков, печей и шахт.
- Вы можете выбрать из доступных вариантов, включая предыдущие уровни.
- При покупке оборудование помечается как *(Куплено)*, и вы можете бесплатно переключаться между купленными предметами.
- При покупке оборудования отображаются его характеристики.

6️⃣ *Как узнать свой баланс и содержимое портфеля?*
- Нажмите на 💎 Баланс или 🎒 Мой портфель в главном меню.
- Чем выше уровень вашего *портфеля*, тем больше руды вы можете носить с собой.

7️⃣ *🔴 Админ панель 🔴:*
- Доступна только администратору бота.
- Позволяет управлять пользователями: добавлять/убирать баланс, удалять пользователей и просматривать список активных игроков.

8️⃣ *Что делать, если бот не реагирует на команды?*
- Используйте кнопку ⏪ Меню, чтобы вернуться в главное меню или перезапустите бота.

9️⃣ *Как получить больше угля?*
- Уголь можно добывать вместе с рудой, при выборе для переплавки.
- Вы можете добавлять уголь в печь неограниченно, сколько захотите.

🔟 *Есть ли ограничение на уровень оборудования?*
- Да, каждый тип оборудования имеет максимальный уровень.

1️⃣1️⃣ *Как открыть новые планеты?*
- В магазине доступна вкладка "Купить планеты" для приобретения Луна и Марс за 150,000 и 350,000 монет соответственно.
- После покупки планеты вы сможете бесплатно переключаться между Луной и Марсом.
- Открыв планету, вы получите доступ к её уникальному магазину с более дорогими предметами и увеличенными наградами.

1️⃣2️⃣ *Что такое Ребирты?*
- Ребирты позволяют вам сбросить весь прогресс в игре (баланс, купленные предметы, планеты и т.д.) в обмен на увеличенный множитель монет.
- Каждый новый ребирт увеличивает ваш множитель монет на ×1.
- Например, после первого ребирта множитель будет ×2, после второго ×3 и т.д.
- Ребирты можно покупать только на планете Марс.
- Максимальное количество ребиртов: 10.

1️⃣3️⃣ *Что такое Геймпассы?*
- Геймпассы предоставляют специальные бонусы и улучшения, такие как увеличение удачи или удвоение добываемой руды.
- Вы можете приобрести геймпассы за монеты в разделе *Геймпассы*.
- Геймпассы не сбрасываются при ребиртах.

1️⃣4️⃣ *Что такое Кликер и Майнеры?*
- *Кликер* позволяет вам получать 1 монету за каждый клик с ограничением в 1 клик каждые 2 секунды. Игра доступна через синюю кнопку *Open App*.
- *Майнеры* обеспечивают пассивный доход монет в зависимости от их уровня и стоимости. Майнеры приносят прибыль каждые 10 часов.
- Вы можете разблокировать вкладку *Кликер и Майнеры* за 65,000 монет.
- Майнеры можно включать и отключать в любое время.
    
*Для возврата в главное меню используйте кнопку ⏪ Меню.*

*Описание планет:*

🌍 *Земля:*
- Начальная планета с базовыми предметами и рудой.

🌕 *Луна:*
- Дополнительная планета с уникальными предметами и рудой.

🔴 *Марс:*
- Стоимость: 350,000 монет.
- Уникальные предметы: Марсианские кирки, рюкзаки, печи и шахты.
- Руды на Марсе имеют уникальные названия и продаются дороже, чем на Луне.
- Ребирты доступны только на Марсе.

*Описание ребиртов:*

🔹 *Ребирты:*
- Позволяют сбросить весь прогресс в игре.
- Каждый ребирт увеличивает ваш множитель монет на ×1.
- Ребирты продаются исключительно на планете Марс.
- Максимальное количество ребиртов: 10.

🔹 *Геймпассы:*
- Предоставляют специальные бонусы и улучшения.
- Геймпассы не сбрасываются при ребиртах.

🔹 *Кликер и Майнеры:*
- Позволяют получать монеты активным и пассивным способом.
- Кликер: 1 монета за клик раз в 2 секунды.
- Майнеры: Пассивный доход монет каждые 10 часов в зависимости от уровня.
    """
    bot.send_message(message.chat.id, faq_text, parse_mode='Markdown')

# Команда админ-панели
@bot.message_handler(func=lambda message: message.text == '🔴 Админ панель 🔴')
def admin_panel(message):
    user_id = message.from_user.id
    with user_data_lock:
        if user_id == ADMIN_TELEGRAM_ID:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            add_balance_button = types.KeyboardButton('Добавить баланс пользователю')
            remove_balance_button = types.KeyboardButton('Убрать баланс у пользователя')
            delete_user_button = types.KeyboardButton('Удалить пользователя из бота')
            view_users_button = types.KeyboardButton('Просмотреть пользователей')
            back_button = types.KeyboardButton('⏪ Меню')
            markup.add(add_balance_button, remove_balance_button)
            markup.add(delete_user_button, view_users_button)
            markup.add(back_button)
            # Оформление заголовка админ-панели
            admin_header = "🔴 *АДМИН ПАНЕЛЬ* 🔴"
            bot.send_message(message.chat.id, admin_header, reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(message, admin_commands)
        else:
            bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

def admin_commands(message):
    if message.text == 'Добавить баланс пользователю':
        bot.send_message(message.chat.id, "Введите ID пользователя, которому вы хотите добавить баланс:")
        bot.register_next_step_handler(message, add_balance_to_user)
    elif message.text == 'Убрать баланс у пользователя':
        bot.send_message(message.chat.id, "Введите ID пользователя, у которого вы хотите убрать баланс:")
        bot.register_next_step_handler(message, remove_balance_from_user)
    elif message.text == 'Удалить пользователя из бота':
        bot.send_message(message.chat.id, "Введите ID пользователя, которого вы хотите удалить:")
        bot.register_next_step_handler(message, delete_user)
    elif message.text == 'Просмотреть пользователей':
        with user_data_lock:
            if not user_data:
                users_list = "Нет активных пользователей."
            else:
                users_list = "Список пользователей:\n"
                for uid, data in user_data.items():
                    users_list += f"ID: {uid}, Планета: {data['current_planet']}, Баланс: {data['balance']} монет, Ребирты: {data['rebirth_count']}\n"
        bot.send_message(message.chat.id, users_list)
        admin_panel(message)
    elif message.text == '⏪ Меню':
        show_main_menu(message)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Возвращаюсь в админ-панель.")
        admin_panel(message)

def add_balance_to_user(message):
    try:
        target_user_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ID пользователя. Возвращаюсь в админ-панель.")
        admin_panel(message)
        return

    with user_data_lock:
        if target_user_id in user_data:
            bot.send_message(message.chat.id, f"Введите сумму, которую вы хотите добавить пользователю {target_user_id}:")
            bot.register_next_step_handler(message, process_add_balance, target_user_id)
        else:
            bot.send_message(message.chat.id, "Пользователь не найден. Возвращаюсь в админ-панель.")
            admin_panel(message)

def process_add_balance(message, target_user_id):
    try:
        amount = int(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительной.")
            admin_panel(message)
            return
    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Возвращаюсь в админ-панель.")
        admin_panel(message)
        return

    with user_data_lock:
        user_data[target_user_id]['balance'] += amount
    bot.send_message(message.chat.id, f"Пользователю {target_user_id} добавлено {amount} монет.")
    try:
        bot.send_message(target_user_id, f"Администратор добавил вам {amount} монет.")
    except Exception:
        pass  # Если пользователь не найден или не может получить сообщение
    admin_panel(message)

def remove_balance_from_user(message):
    try:
        target_user_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ID пользователя. Возвращаюсь в админ-панель.")
        admin_panel(message)
        return

    with user_data_lock:
        if target_user_id in user_data:
            bot.send_message(message.chat.id, f"Введите сумму, которую вы хотите убрать у пользователя {target_user_id}:")
            bot.register_next_step_handler(message, process_remove_balance, target_user_id)
        else:
            bot.send_message(message.chat.id, "Пользователь не найден. Возвращаюсь в админ-панель.")
            admin_panel(message)

def process_remove_balance(message, target_user_id):
    try:
        amount = int(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительной.")
            admin_panel(message)
            return
    except ValueError:
        bot.send_message(message.chat.id, "Некорректная сумма. Возвращаюсь в админ-панель.")
        admin_panel(message)
        return

    with user_data_lock:
        if user_data[target_user_id]['balance'] < amount:
            bot.send_message(message.chat.id, f"У пользователя {target_user_id} недостаточно средств. Текущий баланс: {user_data[target_user_id]['balance']} монет.")
        else:
            user_data[target_user_id]['balance'] -= amount
            bot.send_message(message.chat.id, f"У пользователя {target_user_id} убрано {amount} монет.")
            try:
                bot.send_message(target_user_id, f"Администратор убрал у вас {amount} монет.")
            except Exception:
                pass  # Если пользователь не найден или не может получить сообщение
    admin_panel(message)

def delete_user(message):
    try:
        target_user_id = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ID пользователя. Возвращаюсь в админ-панель.")
        admin_panel(message)
        return

    with user_data_lock:
        if target_user_id in user_data:
            del user_data[target_user_id]
            bot.send_message(message.chat.id, f"Пользователь {target_user_id} удалён из бота.")
            try:
                bot.send_message(target_user_id, "Ваш профиль был удалён администратором.")
            except Exception:
                pass  # Если пользователь не найден или не может получить сообщение
        else:
            bot.send_message(message.chat.id, "Пользователь не найден. Возвращаюсь в админ-панель.")
    admin_panel(message)

# Основной обработчик сообщений
@bot.message_handler(func=lambda message: True)
def main_handler(message):
    user_id = message.from_user.id
    with user_data_lock:
        if user_id not in user_data:
            # Инициализируем пользователя, если он не был инициализирован ранее
            user_data[user_id] = {
                'current_planet': 'Earth',
                'purchased_planets': ['Earth'],
                'pickaxe_level': {'Earth': 1},
                'backpack_level': {'Earth': 1},
                'furnace_level': {'Earth': 1},
                'mine_level': {'Earth': 1},
                'balance': 0,
                'ores': {'Earth': {}, 'Moon': {}, 'Mars': {}},
                'smelting': {'Earth': {}, 'Moon': {}, 'Mars': {}},
                'coal': {'Earth': 0, 'Moon': 0, 'Mars': 0},
                'is_mining': {'Earth': False, 'Moon': False, 'Mars': False},
                'purchased_pickaxes': {'Earth': [1], 'Moon': [], 'Mars': []},
                'purchased_backpacks': {'Earth': [1], 'Moon': [], 'Mars': []},
                'purchased_furnaces': {'Earth': [1], 'Moon': [], 'Mars': []},
                'purchased_mines': {'Earth': [1], 'Moon': [], 'Mars': []},
                'ingots': {'Earth': {}, 'Moon': {}, 'Mars': {}},
                'rebirth_count': 0,
                'multiplier': 1,
                'game_passes': {},
                'clicker': {
                    'enabled': False,
                    'last_click_time': 0
                },
                'miners_owned': []
            }

    current_planet = user_data[user_id]['current_planet']

    # Обработка различных команд и кнопок
    if message.text == '⛏ Добывать руду':
        start_mining(message)
    elif message.text == '🔥 Печь':
        furnace_menu(message)
    elif message.text == '💰 Продать руду':
        sell_ores(message)
    elif message.text == '🛒 Магазин':
        shop_menu(message)
    elif message.text == '💎 Баланс':
        show_balance(message)
    elif message.text == '🎒 Мой портфель':
        show_inventory(message)
    elif message.text == '❓ Помощь':
        show_help(message)
    elif message.text == '🔄 Переключиться на планету':
        switch_planet_menu(message)
    elif message.text.startswith('Купить ') and not message.text.startswith('Купить ребирт') and message.text != 'Купить планеты' and message.text not in ['Купить Марс', 'Купить Луну']:
        item_type = message.text.split('Купить ')[1].lower()
        if item_type == 'кирку':
            buy_pickaxe(message)
        elif item_type == 'рюкзак':
            buy_backpack(message)
        elif item_type == 'печь':
            buy_furnace(message)
        elif item_type == 'шахту':
            buy_mine(message)
        elif item_type == 'кейсы':
            show_cases_menu(message)
        else:
            bot.send_message(message.chat.id, "Неизвестный тип товара. Используйте кнопки магазина.")
    elif message.text.startswith('Купить ребирт'):
        buy_rebirth(message)
    elif message.text.startswith('Купить планеты'):
        buy_planets_menu(message)
    elif message.text.startswith('Кликнуть') or message.text == 'Клик':
        handle_click(message)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Используйте кнопку ⏪ Меню для возврата в главное меню.")

# Функция начала добычи
def start_mining(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        if user_data[user_id].get('is_mining', {}).get(current_planet, False):
            bot.send_message(message.chat.id, "Не флуди! Подождите, пока добыча руды завершится.")
            return
        user_data[user_id]['is_mining'][current_planet] = True  # Устанавливаем флаг добычи
    bot.send_message(message.chat.id, f"Вы начали добычу руды на планете {current_planet}...")
    threading.Thread(target=mine_ore, args=(message,)).start()

# Функция добычи руды с увеличением шанса на более ценную руду при повышении уровня шахты
def mine_ore(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    time.sleep(3)  # Добыча руды занимает 3 секунды

    with user_data_lock:
        pickaxe_level = user_data[user_id]['pickaxe_level'][current_planet]
        mine_level = user_data[user_id]['mine_level'][current_planet]
        backpack_level = user_data[user_id]['backpack_level'][current_planet]
        backpack_capacity = get_backpack_capacity(user_id, current_planet)
        pickaxe_luck = get_pickaxe_luck(user_id, current_planet)
        game_passes = user_data[user_id]['game_passes']

        # Применение геймпассов
        if 'Удвоение Удачи' in game_passes:
            pickaxe_luck *= 2
        if 'Ультра Удача' in game_passes:
            pickaxe_luck *= 5

    # Определение количества добытой руды
    if pickaxe_level <= 3:
        amount = random.randint(1, 3)
    elif 3 < pickaxe_level <= 7:
        amount = random.randint(1, 5)
    else:
        amount = random.randint(2, 7)

    # Применение геймпасс "Двойная руда"
    if 'Двойная Руда' in game_passes:
        amount *= 2

    # Получение списка руд на текущей планете
    ore_list = ores[current_planet]
    base_weights = [ore['weight'] for ore in ore_list]

    # Увеличение веса более ценных руд на уровне шахты
    total_ores = len(ore_list)
    modified_weights = []
    for idx, ore in enumerate(ore_list):
        # Определяем, насколько ценной является руда
        # Чем выше индекс, тем ценнее руда
        # Расчитываем долю ценности
        value_fraction = (idx + 1) / total_ores  # от 1/total до 1
        # Определяем модификатор на основе уровня шахты
        # Например, каждый уровень шахты добавляет 5% к весу пропорционально ценности руды
        modifier = 1 + (mine_level * 0.05 * value_fraction)
        modified_weight = ore['weight'] * modifier
        modified_weights.append(modified_weight)

    # Выбор руды на основе модифицированных весов
    mined_ore = random.choices(ore_list, weights=modified_weights, k=1)[0]['name']

    with user_data_lock:
        current_ores = sum(user_data[user_id]['ores'][current_planet].values())
        if current_ores + amount > backpack_capacity:
            amount = backpack_capacity - current_ores
            if amount <= 0:
                bot.send_message(message.chat.id, "Ваш портфель переполнен!")
                user_data[user_id]['is_mining'][current_planet] = False
                return
        user_data[user_id]['ores'][current_planet][mined_ore] = user_data[user_id]['ores'][current_planet].get(mined_ore, 0) + amount

    bot.send_message(message.chat.id, f"Вы добыли {amount} x {mined_ore} на планете {current_planet}.")
    with user_data_lock:
        user_data[user_id]['is_mining'][current_planet] = False

def get_backpack_capacity(user_id, planet):
    backpack_level = user_data[user_id]['backpack_level'][planet]
    return backpacks[planet][backpack_level - 1]['capacity']

def get_pickaxe_luck(user_id, planet):
    pickaxe_level = user_data[user_id]['pickaxe_level'][planet]
    return pickaxes[planet][pickaxe_level - 1]['luck']

# Меню печи
def furnace_menu(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_coal_button = types.KeyboardButton('➕ Добавить уголь')
    smelt_ore_button = types.KeyboardButton('⚒ Переплавить руду')
    back_button = types.KeyboardButton('⏪ Меню')
    markup.add(add_coal_button, smelt_ore_button)
    markup.add(back_button)

    with user_data_lock:
        ores_available = user_data[user_id]['ores'][current_planet].copy()

    if ores_available:
        ores_list = "Доступные для переплавки руды:\n"
        for ore, amount in ores_available.items():
            ores_list += f"{ore}: {amount} шт.\n"
        ores_list += "\nВыберите действие:"
        bot.send_message(message.chat.id, ores_list, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"В вашем портфеле на планете {current_planet} нет руды для переплавки.", reply_markup=markup)

# Добавить уголь
@bot.message_handler(func=lambda message: message.text == '➕ Добавить уголь')
def add_coal(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    bot.send_message(message.chat.id, f"Сколько угля вы хотите добавить в печь на планете {current_planet}?")
    bot.register_next_step_handler(message, process_add_coal)

def process_add_coal(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    try:
        amount = int(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, "Количество должно быть положительным.")
            return
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        return

    with user_data_lock:
        user_data[user_id]['coal'][current_planet] += amount
    bot.send_message(message.chat.id, f"Вы добавили {amount} угля в печь на планете {current_planet}.")

# Переплавить руду
@bot.message_handler(func=lambda message: message.text == '⚒ Переплавить руду')
def smelt_ore(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        ores_user = user_data[user_id]['ores'][current_planet].copy()
    if not ores_user:
        bot.send_message(message.chat.id, "У вас нет руды для переплавки.")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for ore, amount in ores_user.items():
        markup.add(types.KeyboardButton(f"{ore} {amount} шт."))
    back_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button)
    bot.send_message(message.chat.id, f"Выберите руду для переплавки на планете {current_planet}:", reply_markup=markup)
    bot.register_next_step_handler(message, process_smelt_ore)

def process_smelt_ore(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    selected_text = message.text
    if selected_text == '⏪ Меню':
        show_main_menu(message)
        return
    # Извлекаем название руды из текста кнопки, например, "Железная руда 3 шт." -> "Железная руда"
    if ' шт.' in selected_text:
        ore = selected_text.rsplit(' ', 2)[0]
    else:
        ore = selected_text  # На всякий случай

    with user_data_lock:
        if ore not in user_data[user_id]['ores'][current_planet]:
            bot.send_message(message.chat.id, "У вас нет такой руды.")
            return
        if user_data[user_id]['coal'][current_planet] <= 0:
            bot.send_message(message.chat.id, "У вас нет угля для переплавки.")
            return
    bot.send_message(message.chat.id, f"Сколько '{ore}' вы хотите переплавить на планете {current_planet}?")
    with user_data_lock:
        user_data[user_id]['selected_ore'] = ore
    bot.register_next_step_handler(message, process_smelting_amount)

def process_smelting_amount(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    try:
        amount = int(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, "Количество должно быть положительным.")
            return
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        return

    with user_data_lock:
        ore = user_data[user_id].get('selected_ore')
        if not ore:
            bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте снова.")
            return
        available_amount = user_data[user_id]['ores'][current_planet].get(ore, 0)
        if amount > available_amount:
            bot.send_message(message.chat.id, f"У вас нет столько '{ore}'. Доступно для переплавки: {available_amount}.")
            return
        if user_data[user_id]['coal'][current_planet] <= 0:
            bot.send_message(message.chat.id, "У вас нет угля для переплавки.")
            return
        furnace_level = user_data[user_id]['furnace_level'][current_planet]
        smelting_capacity = furnaces[current_planet][furnace_level - 1]['smelt_capacity']
        if amount > smelting_capacity:
            bot.send_message(message.chat.id, f"Ваша печь может переплавить за раз не более {smelting_capacity} единиц руды.")
            amount = smelting_capacity
        # Проверка геймпасса "Моментальная переплавка"
        smelt_time = 0 if 'Моментальная Переплавка' in user_data[user_id]['game_passes'] else 3
        # Обновляем данные пользователя
        user_data[user_id]['ores'][current_planet][ore] -= amount
        if user_data[user_id]['ores'][current_planet][ore] == 0:
            del user_data[user_id]['ores'][current_planet][ore]
        user_data[user_id]['smelting'][current_planet][ore] = user_data[user_id]['smelting'][current_planet].get(ore, 0) + amount
        user_data[user_id]['coal'][current_planet] -= 1
    bot.send_message(message.chat.id, f"Начата переплавка {amount} x {ore} на планете {current_planet}. Это займет {smelt_time} секунд.")
    threading.Thread(target=finish_smelting, args=(message, ore, amount, smelt_time)).start()

def finish_smelting(message, ore, amount, smelt_time):
    try:
        time.sleep(smelt_time)
        user_id = message.from_user.id
        current_planet = user_data[user_id]['current_planet']
        with user_data_lock:
            user_data[user_id]['smelting'][current_planet][ore] -= amount
            if user_data[user_id]['smelting'][current_planet][ore] == 0:
                del user_data[user_id]['smelting'][current_planet][ore]
            user_data[user_id]['ingots'][current_planet][ore] = user_data[user_id]['ingots'][current_planet].get(ore, 0) + amount
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при переплавке: {e}")
        with user_data_lock:
            user_data[user_id]['is_mining'][current_planet] = False
        admin_panel(message)
    finally:
        bot.send_message(message.chat.id, f"Переплавка {amount} x {ore} на планете {current_planet} завершена.")
        # Автоматический возврат в меню печи после завершения переплавки
        furnace_menu(message)

# Продать руду
@bot.message_handler(func=lambda message: message.text == '💰 Продать руду')
def sell_ores(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        ingots = user_data[user_id]['ingots'][current_planet].copy()
    if not ingots:
        bot.send_message(message.chat.id, "У вас нет переплавленной руды для продажи.")
        return
    total_earnings = 0
    earnings_details = ""
    earth_ores = [ore_item['name'] for ore_item in ores['Earth']]
    with user_data_lock:
        for ore, amount in ingots.items():
            if ore in earth_ores:
                base_price = 10 * (earth_ores.index(ore) + 1)
            else:
                base_price = 10  # Можно настроить по желанию
            if current_planet == 'Earth':
                multiplier = 1
            elif current_planet == 'Moon':
                multiplier = 1.5
            elif current_planet == 'Mars':
                multiplier = 2
            earnings = int(amount * base_price * multiplier * user_data[user_id]['multiplier'])
            total_earnings += earnings
            earnings_details += f"{ore}: {amount} x {base_price} x {multiplier} x {user_data[user_id]['multiplier']} = {earnings} монет\n"
        user_data[user_id]['balance'] += total_earnings
        user_data[user_id]['ingots'][current_planet] = {}
    sell_message = f"Вы продали все переплавленные руды на планете {current_planet} и заработали {total_earnings} монет.\n\nДетали:\n{earnings_details}"
    bot.send_message(message.chat.id, sell_message)

# Показать баланс
def show_balance(message):
    user_id = message.from_user.id
    with user_data_lock:
        balance = user_data[user_id]['balance']
        multiplier = user_data[user_id]['multiplier']
    bot.send_message(message.chat.id, f"Ваш баланс: {balance} монет.\nМножитель монет: ×{multiplier}")

# Показать портфель
@bot.message_handler(func=lambda message: message.text == '🎒 Мой портфель')
def show_inventory(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        ores_in_inventory = user_data[user_id]['ores'][current_planet].copy()
        ingots = user_data[user_id]['ingots'][current_planet].copy()
    if not ores_in_inventory and not ingots:
        bot.send_message(message.chat.id, f"Ваш портфель на планете {current_planet} пуст.")
    else:
        inventory = f"Портфель содержит:\n"
        if ores_in_inventory:
            inventory += "\n*Не переплавленной руды:*\n"
            for ore, amount in ores_in_inventory.items():
                inventory += f"{ore}: {amount} шт.\n"
        else:
            inventory += "\n*Не переплавленной руды:* Нет\n"
        
        if ingots:
            inventory += "\n*Переплавленной руды:*\n"
            for ore, amount in ingots.items():
                inventory += f"{ore}: {amount} шт.\n"
        else:
            inventory += "\n*Переплавленной руды:* Нет\n"
        
        bot.send_message(message.chat.id, inventory, parse_mode='Markdown')

# Меню магазина с отдельной вкладкой для покупки планет и ребиртов
def shop_menu(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        rebirth_available = current_planet == 'Mars' and user_data[user_id]['rebirth_count'] < len(rebirths)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buy_pickaxe_button = types.KeyboardButton('Купить кирку')
    buy_backpack_button = types.KeyboardButton('Купить рюкзак')
    buy_furnace_button = types.KeyboardButton('Купить печь')
    buy_mine_button = types.KeyboardButton('Купить шахту')
    buy_cases_button = types.KeyboardButton('Кейсы')  # Убраны смайлики
    buy_rebirth_button = types.KeyboardButton('Купить ребирт') if rebirth_available else None
    buy_planets_button = types.KeyboardButton('Купить планеты')  # Новая кнопка для покупки планет
    back_button = types.KeyboardButton('⏪ Меню')
    
    # Добавляем кнопки в магазин
    buttons = [buy_pickaxe_button, buy_backpack_button]
    buttons += [buy_furnace_button, buy_mine_button]
    buttons += [buy_cases_button]
    if buy_rebirth_button:
        buttons.append(buy_rebirth_button)
    buttons.append(buy_planets_button)
    buttons.append(back_button)
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, f"Магазин на планете {current_planet}", reply_markup=markup)

# Функция покупки и переключения оборудования
def buy_pickaxe(message):
    buy_item(message, 'pickaxe')

def buy_backpack(message):
    buy_item(message, 'backpack')

def buy_furnace(message):
    buy_item(message, 'furnace')

def buy_mine(message):
    buy_item(message, 'mine')

def buy_item(message, item_type):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        if item_type == 'pickaxe':
            items = pickaxes[current_planet]
            user_inventory = user_data[user_id]['purchased_pickaxes'][current_planet]
            current_level = user_data[user_id]['pickaxe_level'][current_planet]
            price_multiplier = 450 if current_planet == 'Earth' else (675 if current_planet == 'Moon' else 900)  # Увеличены цены на 1.5x
        elif item_type == 'backpack':
            items = backpacks[current_planet]
            user_inventory = user_data[user_id]['purchased_backpacks'][current_planet]
            current_level = user_data[user_id]['backpack_level'][current_planet]
            price_multiplier = 450 if current_planet == 'Earth' else (675 if current_planet == 'Moon' else 900)
        elif item_type == 'furnace':
            items = furnaces[current_planet]
            user_inventory = user_data[user_id]['purchased_furnaces'][current_planet]
            current_level = user_data[user_id]['furnace_level'][current_planet]
            price_multiplier = 600 if current_planet == 'Earth' else (900 if current_planet == 'Moon' else 1200)
        elif item_type == 'mine':
            items = miners
            user_inventory = user_data[user_id]['miners_owned']
            current_level = len(user_inventory)
            price_multiplier = 7500 * (current_level + 1)  # Цены указаны напрямую
        else:
            return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for idx, item in enumerate(items):
        level = idx + 1
        if item_type == 'mine':
            item_name = item['name']
            price = item['price']
            earn = item['earn_per_10_hours']
            if item_name in user_inventory:
                label = f"{item_name} (Куплено)"
            else:
                label = f"{item_name} - {price} монет"
        else:
            item_name = item['name']
            price = item['price'] * price_multiplier
            if item_type == 'pickaxe':
                label = f"{item_name} (+{item['luck']}% удачи) - {price} монет"
            elif item_type == 'backpack':
                label = f"{item_name} (вместимость: {item['capacity']}) - {price} монет"
            elif item_type == 'furnace':
                label = f"{item_name} (переплавка: {item['smelt_capacity']} руд) - {price} монет"
        markup.add(types.KeyboardButton(label))
    back_button = types.KeyboardButton('🛒 Продолжить покупки')
    exit_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button, exit_button)
    if item_type == 'mine':
        bot.send_message(message.chat.id, f"Выберите майнера для покупки на планете {current_planet}:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"Выберите {item_type} на планете {current_planet}:", reply_markup=markup)
    bot.register_next_step_handler(message, process_buy_item, item_type, items, price_multiplier)

def process_buy_item(message, item_type, items, price_multiplier):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    selected = message.text
    if selected == '⏪ Меню':
        show_main_menu(message)
        return
    elif selected == '🛒 Продолжить покупки':
        shop_menu(message)
        return

    with user_data_lock:
        if item_type == 'mine':
            selected_miner = next((miner for miner in miners if f"{miner['name']} - {miner['price']} монет" == selected), None)
            if not selected_miner:
                bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню майнеров.")
                show_clicker_miners_menu(message)
                return
            if selected_miner['name'] in user_data[user_id]['miners_owned']:
                bot.send_message(message.chat.id, f"Вы уже приобрели майнера '{selected_miner['name']}'.")
                return
            if user_data[user_id]['balance'] < selected_miner['price']:
                bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки майнера '{selected_miner['name']}'. Нужно {selected_miner['price']} монет.")
                return
            # Покупка майнера
            user_data[user_id]['balance'] -= selected_miner['price']
            user_data[user_id]['miners_owned'].append(selected_miner['name'])
            # Запуск пассивного дохода
            threading.Thread(target=passive_income, args=(user_id, selected_miner)).start()
            bot.send_message(message.chat.id, f"Вы успешно приобрели майнера '{selected_miner['name']}' за {selected_miner['price']} монет.")
        else:
            # Для других типов предметов
            selected_item = next((item for item in items if (item_type != 'mine' and f"{item['name']} (+{item.get('luck', 0)}% удачи) - {item['price'] * price_multiplier} монет" == selected) or 
                                 (item_type == 'backpack' and f"{item['name']} (вместимость: {item['capacity']}) - {item['price'] * price_multiplier} монет" == selected) or
                                 (item_type == 'furnace' and f"{item['name']} (переплавка: {item['smelt_capacity']} руд) - {item['price'] * price_multiplier} монет" == selected)) , None)
            if not selected_item:
                bot.send_message(message.chat.id, "Некорректный выбор. Попробуйте снова.")
                buy_item(message, item_type)
                return
            price = selected_item['price'] * price_multiplier
            if item_type == 'pickaxe':
                if selected_item['name'] in user_data[user_id]['purchased_pickaxes'][current_planet]:
                    # Переключение на уже купленную кирку
                    user_data[user_id]['pickaxe_level'][current_planet] = pickaxes[current_planet].index(selected_item) + 1
                    bot.send_message(message.chat.id, f"Вы переключились на {selected_item['name']} на планете {current_planet}.")
                    return
            elif item_type == 'backpack':
                if selected_item['name'] in user_data[user_id]['purchased_backpacks'][current_planet]:
                    # Переключение на уже купленный рюкзак
                    user_data[user_id]['backpack_level'][current_planet] = backpacks[current_planet].index(selected_item) + 1
                    bot.send_message(message.chat.id, f"Вы переключились на {selected_item['name']} на планете {current_planet}.")
                    return
            elif item_type == 'furnace':
                if selected_item['name'] in user_data[user_id]['purchased_furnaces'][current_planet]:
                    # Переключение на уже купленную печь
                    user_data[user_id]['furnace_level'][current_planet] = furnaces[current_planet].index(selected_item) + 1
                    bot.send_message(message.chat.id, f"Вы переключились на {selected_item['name']} на планете {current_planet}.")
                    return

            # Покупка предмета
            if user_data[user_id]['balance'] < price:
                bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки {selected_item['name']}. Нужно {price} монет.")
                return
            user_data[user_id]['balance'] -= price
            if item_type == 'pickaxe':
                user_data[user_id]['pickaxe_level'][current_planet] = pickaxes[current_planet].index(selected_item) + 1
                user_data[user_id]['purchased_pickaxes'][current_planet].append(selected_item['name'])
            elif item_type == 'backpack':
                user_data[user_id]['backpack_level'][current_planet] = backpacks[current_planet].index(selected_item) + 1
                user_data[user_id]['purchased_backpacks'][current_planet].append(selected_item['name'])
            elif item_type == 'furnace':
                user_data[user_id]['furnace_level'][current_planet] = furnaces[current_planet].index(selected_item) + 1
                user_data[user_id]['purchased_furnaces'][current_planet].append(selected_item['name'])
            bot.send_message(message.chat.id, f"Вы купили {selected_item['name']} за {price} монет на планете {current_planet}.")

    bot.send_message(message.chat.id, "Неизвестный тип товара. Используйте кнопки магазина.")

# Функция пассивного дохода от майнеров каждые 10 часов
def passive_income(user_id, miner):
    while True:
        time.sleep(36000)  # 10 часов = 36000 секунд
        with user_data_lock:
            if miner['name'] in user_data[user_id]['miners_owned']:
                earnings = miner['earn_per_10_hours'] * user_data[user_id]['multiplier']
                user_data[user_id]['balance'] += earnings
                bot.send_message(user_id, f"Ваш майнер '{miner['name']}' принес вам {earnings} монет.")
            else:
                break  # Если майнер продан или удалён

# Меню для кликера и майнеров
def show_clicker_miners_menu(message):
    user_id = message.from_user.id
    with user_data_lock:
        if not user_data[user_id]['clicker']['enabled']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            unlock_button = types.KeyboardButton('🔓 Разблокировать Кликер и Майнеры - 65,000 монет')
            back_button = types.KeyboardButton('⏪ Меню')
            markup.add(unlock_button)
            markup.add(back_button)
            bot.send_message(message.chat.id, "Вкладка *Кликер и Майнеры* ещё не разблокирована. Разблокируйте её за 65,000 монет, чтобы начать зарабатывать активные и пассивные монеты.", reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(message, process_unlock_clicker_miners)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            click_button = types.KeyboardButton('👆 Кликнуть')
            toggle_miners_button = types.KeyboardButton('🔄 Включить/Выключить Майнеров')
            buy_miners_button = types.KeyboardButton('🛒 Купить Майнеров')
            back_button = types.KeyboardButton('⏪ Меню')
            markup.add(click_button, toggle_miners_button)
            markup.add(buy_miners_button)
            markup.add(back_button)
            bot.send_message(message.chat.id, "Вкладка *Кликер и Майнеры* активна.\n\n*Кликер:* Нажмите '👆 Кликнуть' раз в 2 секунды, чтобы получить 1 монету.\n*Майнеры:* Автоматически приносят монеты каждые 10 часов.", reply_markup=markup, parse_mode='Markdown')

def process_unlock_clicker_miners(message):
    user_id = message.from_user.id
    selected = message.text
    if selected.startswith('🔓 Разблокировать'):
        with user_data_lock:
            price = 65000
            if user_data[user_id]['balance'] < price:
                bot.send_message(message.chat.id, f"У вас недостаточно монет для разблокировки Кликера и Майнеров. Нужно {price} монет.")
                show_clicker_miners_menu(message)
                return
            user_data[user_id]['balance'] -= price
            user_data[user_id]['clicker']['enabled'] = True
        bot.send_message(message.chat.id, "Вы успешно разблокировали *Кликер и Майнеры*!", parse_mode='Markdown')
        show_clicker_miners_menu(message)
    elif selected == '⏪ Меню':
        show_main_menu(message)
    else:
        bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню Кликера и Майнеров.")
        show_clicker_miners_menu(message)

# Обработка клика
@bot.message_handler(func=lambda message: message.text == '👆 Кликнуть')
def handle_click(message):
    user_id = message.from_user.id
    current_time = time.time()
    with user_data_lock:
        last_click = user_data[user_id]['clicker']['last_click_time']
        if current_time - last_click < 2:
            remaining = int(2 - (current_time - last_click))
            bot.send_message(message.chat.id, f"Пожалуйста, подождите {remaining} секунд перед следующим кликом.")
            return
        user_data[user_id]['clicker']['last_click_time'] = current_time
        user_data[user_id]['balance'] += 1
    bot.send_message(message.chat.id, "Вы получили 1 монету!")

# Меню для покупки майнеров через вкладку Кликер и Майнеры
@bot.message_handler(func=lambda message: message.text == '🛒 Купить Майнеров')
def buy_miners(message):
    user_id = message.from_user.id
    with user_data_lock:
        owned_miners = user_data[user_id]['miners_owned']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for miner in miners:
        label = f"Купить {miner['name']} - {miner['price']} монет"
        markup.add(types.KeyboardButton(label))
    back_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button)
    bot.send_message(message.chat.id, "Выберите майнера для покупки:", reply_markup=markup)
    bot.register_next_step_handler(message, process_buy_miner)

def process_buy_miner(message):
    user_id = message.from_user.id
    selected = message.text
    if selected == '⏪ Меню':
        show_main_menu(message)
        return
    # Найти выбранный майнер
    selected_miner = next((miner for miner in miners if f"Купить {miner['name']} - {miner['price']} монет" == selected), None)
    if not selected_miner:
        bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню покупки майнеров.")
        buy_miners(message)
        return
    with user_data_lock:
        if selected_miner['name'] in user_data[user_id]['miners_owned']:
            bot.send_message(message.chat.id, f"Вы уже приобрели майнера '{selected_miner['name']}'.")
            return
        if user_data[user_id]['balance'] < selected_miner['price']:
            bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки майнера '{selected_miner['name']}'. Нужно {selected_miner['price']} монет.")
            return
        # Покупка майнера
        user_data[user_id]['balance'] -= selected_miner['price']
        user_data[user_id]['miners_owned'].append(selected_miner['name'])
        # Запуск пассивного дохода
        threading.Thread(target=passive_income, args=(user_id, selected_miner)).start()
    bot.send_message(message.chat.id, f"Вы успешно приобрели майнера '{selected_miner['name']}' за {selected_miner['price']} монет.")

# Меню кейсов (уровень rudy)
@bot.message_handler(func=lambda message: message.text == 'Кейсы')
def show_cases_menu(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        available_cases = cases[current_planet].copy()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for case in available_cases:
        label = f"{case['name']} - {case['price']} монет"  # Убраны смайлики
        markup.add(types.KeyboardButton(label))
    back_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button)
    bot.send_message(message.chat.id, f"Выберите кейс для покупки и открытия на планете {current_planet}:", reply_markup=markup)
    bot.register_next_step_handler(message, process_case_selection)

def process_case_selection(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    selected = message.text
    if selected == '⏪ Меню':
        show_main_menu(message)
        return

    with user_data_lock:
        selected_case = next((case for case in cases[current_planet] if f"{case['name']} - {case['price']} монет" == selected), None)

    if not selected_case:
        bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню кейсов.")
        show_cases_menu(message)
        return

    with user_data_lock:
        if user_data[user_id]['balance'] < selected_case['price']:
            bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки {selected_case['name']}. Нужно {selected_case['price']} монет.")
            show_cases_menu(message)
            return
        # Покупка кейса
        user_data[user_id]['balance'] -= selected_case['price']

    bot.send_message(message.chat.id, f"Вы приобрели {selected_case['name']} за {selected_case['price']} монет.")
    bot.send_message(message.chat.id, f"Открытие {selected_case['name']} началось! Подождите 10 секунд...")

    # Запуск процесса открытия кейса в отдельном потоке
    threading.Thread(target=open_case, args=(message, selected_case)).start()

def open_case(message, case):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    min_reward = case['min_reward']
    max_reward = case['max_reward']
    try:
        # Имитация кручения чисел (10 секунд)
        for i in range(1, 11):
            with user_data_lock:
                if current_planet == 'Earth':
                    spinning_number = random.randint(min_reward, max_reward)
                elif current_planet == 'Moon':
                    spinning_number = random.randint(int(min_reward * 1.2), int(max_reward * 1.2))  # Увеличение на 20%
                elif current_planet == 'Mars':
                    spinning_number = random.randint(int(min_reward * 1.4), int(max_reward * 1.4))  # Увеличение на 40%
                else:
                    spinning_number = random.randint(min_reward, max_reward)  # По умолчанию
            bot.send_message(message.chat.id, f"🔄 Крутится... {spinning_number} монет")
            time.sleep(1)
        # Генерация окончательной награды
        with user_data_lock:
            if current_planet == 'Earth':
                reward = random.randint(min_reward, max_reward)
            elif current_planet == 'Moon':
                reward = random.randint(int(min_reward * 1.2), int(max_reward * 1.2))
            elif current_planet == 'Mars':
                reward = random.randint(int(min_reward * 1.4), int(max_reward * 1.4))
            else:
                reward = random.randint(min_reward, max_reward)  # По умолчанию
            # Применение множителя монет
            reward *= user_data[user_id]['multiplier']
            user_data[user_id]['balance'] += reward
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при открытии кейса: {e}")
    finally:
        bot.send_message(message.chat.id, f"🎉 Поздравляем! Вы получили {reward} монет из {case['name']} на планете {current_planet}.")
        # Автоматический возврат в меню кейсов после открытия
        show_cases_menu(message)

# Функция покупки ребирта
@bot.message_handler(func=lambda message: message.text.startswith('Купить ребирт'))
def buy_rebirth(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        rebirth_available = current_planet == 'Mars' and user_data[user_id]['rebirth_count'] < len(rebirths)
        if not rebirth_available:
            if current_planet != 'Mars':
                reason = "Ребирты можно покупать только на планете Марс."
            else:
                reason = "Вы достигли максимального количества ребиртов."
            bot.send_message(message.chat.id, reason)
            return
        rebirth = rebirths[user_data[user_id]['rebirth_count']]
        price = rebirth['price']
        if user_data[user_id]['balance'] < price:
            bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки ребирта '{rebirth['name']}'. Нужно {price} монет.")
            return
        # Подтверждение покупки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes_button = types.KeyboardButton('Да')
        no_button = types.KeyboardButton('Нет')
        markup.add(yes_button, no_button)
    bot.send_message(message.chat.id, f"Вы уверены, что хотите купить ребирт '{rebirth['name']}' за {price} монет?\nВсе ваши данные будут сброшены, и баланс станет 0, но ваш множитель монет увеличится на ×1.", reply_markup=markup)
    bot.register_next_step_handler(message, confirm_rebirth_purchase, rebirth)

def confirm_rebirth_purchase(message, rebirth):
    user_id = message.from_user.id
    if message.text.lower() == 'да':
        price = rebirth['price']
        with user_data_lock:
            if user_data[user_id]['balance'] < price:
                bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки ребирта '{rebirth['name']}'. Нужно {price} монет.")
                return
            user_data[user_id]['balance'] -= price
            user_data[user_id]['rebirth_count'] += 1
            user_data[user_id]['multiplier'] += 1
            # Сброс всех данных, кроме rebirth_count, multiplier и game_passes
            user_data[user_id]['current_planet'] = 'Earth'  # После сброса игрок начинает с Земли
            user_data[user_id]['purchased_planets'] = ['Earth']  # Только Земля как купленная планета
            user_data[user_id]['pickaxe_level'] = {'Earth': 1}
            user_data[user_id]['backpack_level'] = {'Earth': 1}
            user_data[user_id]['furnace_level'] = {'Earth': 1}
            user_data[user_id]['mine_level'] = {'Earth': 1}
            user_data[user_id]['purchased_pickaxes'] = {'Earth': [1], 'Moon': [], 'Mars': []}
            user_data[user_id]['purchased_backpacks'] = {'Earth': [1], 'Moon': [], 'Mars': []}
            user_data[user_id]['purchased_furnaces'] = {'Earth': [1], 'Moon': [], 'Mars': []}
            user_data[user_id]['purchased_mines'] = {'Earth': [1], 'Moon': [], 'Mars': []}
            user_data[user_id]['ores'] = {'Earth': {}, 'Moon': {}, 'Mars': {}}
            user_data[user_id]['smelting'] = {'Earth': {}, 'Moon': {}, 'Mars': {}}
            user_data[user_id]['coal'] = {'Earth': 0, 'Moon': 0, 'Mars': 0}
            user_data[user_id]['is_mining'] = {'Earth': False, 'Moon': False, 'Mars': False}
            user_data[user_id]['ingots'] = {'Earth': {}, 'Moon': {}, 'Mars': {}}
            # Очистка выбранной руды
            if 'selected_ore' in user_data[user_id]:
                del user_data[user_id]['selected_ore']
            # Установка баланса в 0 после ребирта
            user_data[user_id]['balance'] = 0
            # Game Passes не сбрасываются
    else:
        bot.send_message(message.chat.id, "Покупка ребирта отменена.")
    show_main_menu(message)

# Функции для отображения и покупки геймпассов (удалены из главного меню, но оставлены для API)
def show_game_passes_menu(message):
    user_id = message.from_user.id
    with user_data_lock:
        available_game_passes = [gp for gp in game_passes.values() if gp['name'] not in user_data[user_id]['game_passes']]
    if not available_game_passes:
        bot.send_message(message.chat.id, "У вас уже куплены все доступные геймпассы.", reply_markup=types.ReplyKeyboardRemove())
        show_main_menu(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for gp in available_game_passes:
        label = f"Купить {gp['name']} - {gp['price']} монет"
        markup.add(types.KeyboardButton(label))
    back_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button)
    bot.send_message(message.chat.id, "Выберите геймпасс для покупки:", reply_markup=markup)
    bot.register_next_step_handler(message, process_game_pass_purchase)

def process_game_pass_purchase(message):
    user_id = message.from_user.id
    selected = message.text
    if selected == '⏪ Меню':
        show_main_menu(message)
        return
    # Найти выбранный геймпасс
    selected_gp = None
    for gp in game_passes.values():
        if selected == f"Купить {gp['name']} - {gp['price']} монет":
            selected_gp = gp
            break
    if not selected_gp:
        bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню геймпассов.")
        show_game_passes_menu(message)
        return
    with user_data_lock:
        if user_data[user_id]['balance'] < selected_gp['price']:
            bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки {selected_gp['name']}. Нужно {selected_gp['price']} монет.")
            show_game_passes_menu(message)
            return
        # Покупка геймпасс
        user_data[user_id]['balance'] -= selected_gp['price']
        user_data[user_id]['game_passes'][selected_gp['name']] = True
    bot.send_message(message.chat.id, f"Вы успешно приобрели геймпасс '{selected_gp['name']}'.")
    # Обновить кнопку в меню геймпассов
    show_game_passes_menu(message)

# Функция покупки планет
def buy_planet(message, planet_name, price):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        if planet_name in user_data[user_id]['purchased_planets']:
            bot.send_message(message.chat.id, f"Вы уже приобрели планету {planet_name}.")
            return
        if user_data[user_id]['balance'] < price:
            bot.send_message(message.chat.id, f"У вас недостаточно монет для покупки планеты {planet_name}. Нужно {price} монет.")
            return
        user_data[user_id]['balance'] -= price
        user_data[user_id]['purchased_planets'].append(planet_name)
        
        # Инициализация оборудования на новой планете
        user_data[user_id]['pickaxe_level'][planet_name] = 1
        user_data[user_id]['backpack_level'][planet_name] = 1
        user_data[user_id]['furnace_level'][planet_name] = 1
        user_data[user_id]['mine_level'][planet_name] = 1
        user_data[user_id]['purchased_pickaxes'][planet_name] = [1]
        user_data[user_id]['purchased_backpacks'][planet_name] = [1]
        user_data[user_id]['purchased_furnaces'][planet_name] = [1]
        user_data[user_id]['purchased_mines'][planet_name] = []
        user_data[user_id]['ores'][planet_name] = {}
        user_data[user_id]['smelting'][planet_name] = {}
        user_data[user_id]['coal'][planet_name] = 0

    bot.send_message(message.chat.id, f"Поздравляем! Вы приобрели планету {planet_name} за {price} монет.")
    bot.send_message(message.chat.id, f"Теперь вы можете переключаться между планетами: {', '.join(user_data[user_id]['purchased_planets'])}.")

# Меню для покупки планет
def buy_planets_menu(message):
    user_id = message.from_user.id
    current_planet = user_data[user_id]['current_planet']
    with user_data_lock:
        available_planets = [planet for planet in ['Moon', 'Mars'] if planet not in user_data[user_id]['purchased_planets']]
    if not available_planets:
        bot.send_message(message.chat.id, "У вас уже куплены все доступные планеты.", reply_markup=types.ReplyKeyboardRemove())
        shop_menu(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for planet in available_planets:
        if planet == 'Moon':
            label = 'Купить Луну'  # Исправлено на корректное название
        else:
            label = 'Купить Марс'  # Оставлено без изменений
        markup.add(types.KeyboardButton(label))
    back_button = types.KeyboardButton('🛒 Продолжить покупки')
    exit_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button, exit_button)
    bot.send_message(message.chat.id, "Выберите планету для покупки:", reply_markup=markup)
    bot.register_next_step_handler(message, process_buy_planet)

def process_buy_planet(message):
    user_id = message.from_user.id
    selected = message.text
    if selected == '⏪ Меню':
        show_main_menu(message)
        return
    elif selected == '🛒 Продолжить покупки':
        shop_menu(message)
        return
    elif selected == 'Купить Луну':
        buy_planet(message, 'Moon', 150000)  # Цена Луна: 150,000 монет
    elif selected == 'Купить Марс':
        buy_planet(message, 'Mars', 350000)  # Цена Марс: 350,000 монет
    else:
        bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню покупки планет.")
        buy_planets_menu(message)

# Функция переключения планеты
@bot.message_handler(func=lambda message: message.text == '🔄 Переключиться на планету')
def switch_planet_menu(message):
    user_id = message.from_user.id
    with user_data_lock:
        purchased_planets = user_data[user_id]['purchased_planets'].copy()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for planet in purchased_planets:
        if planet == 'Earth':
            label = 'Земля'
        elif planet == 'Moon':
            label = 'Луна'
        elif planet == 'Mars':
            label = 'Марс'
        else:
            label = planet
        markup.add(types.KeyboardButton(label))
    back_button = types.KeyboardButton('⏪ Меню')
    markup.add(back_button)
    bot.send_message(message.chat.id, "Выберите планету для переключения:", reply_markup=markup)
    bot.register_next_step_handler(message, process_switch_planet)

def process_switch_planet(message):
    user_id = message.from_user.id
    selected = message.text
    if selected == '⏪ Меню':
        show_main_menu(message)
        return
    planet_mapping = {'Земля': 'Earth', 'Луна': 'Moon', 'Марс': 'Mars'}
    if selected in planet_mapping and planet_mapping[selected] in user_data[user_id]['purchased_planets']:
        with user_data_lock:
            user_data[user_id]['current_planet'] = planet_mapping[selected]
        bot.send_message(message.chat.id, f"Вы переключились на планету {selected}.")
    else:
        bot.send_message(message.chat.id, "Некорректный выбор. Возвращаюсь в меню переключения планет.")
    show_main_menu(message)

# Запуск бота
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Ошибка в работе бота: {e}")
