const coinCountElement = document.getElementById('coin-count');
const clickButton = document.getElementById('click-button');
const upgradeButton = document.getElementById('upgrade-passive');
const gamepassButtons = document.querySelectorAll('.gamepass-button');
const unlockButton = document.getElementById('unlock-button');
const lockDiv = document.getElementById('lock');
const gameDiv = document.getElementById('game');

let coins = 0;
let passiveIncome = 1;
let passiveInterval = 100; // in seconds
let passiveTimer = null;

// Инициализация Telegram Web App
const telegram = window.Telegram.WebApp;
const user_id = telegram.initDataUnsafe.user.id;

// Функция обновления отображения монет
function updateCoinDisplay() {
    coinCountElement.innerText = coins;
}

// Функция для пассивного дохода
function startPassiveIncome() {
    if (passiveTimer) clearInterval(passiveTimer);
    passiveTimer = setInterval(() => {
        coins += passiveIncome;
        updateCoinDisplay();
    }, passiveInterval * 1000);
}

// Обработчик клика
clickButton.addEventListener('click', () => {
    // Ограничение кликов раз в 2 секунды
    if (clickButton.disabled) return;
    coins += 1;
    updateCoinDisplay();
    clickButton.disabled = true;
    setTimeout(() => {
        clickButton.disabled = false;
    }, 2000);
});

// Обработчик улучшения пассивного дохода
upgradeButton.addEventListener('click', () => {
    const upgradeCost = 7500;
    if (coins < upgradeCost) {
        alert('Недостаточно монет для улучшения пассивного дохода.');
        return;
    }
    coins -= upgradeCost;
    passiveIncome += 1;
    passiveInterval = Math.max(1, passiveInterval - 1); // Уменьшаем интервал, минимально 1 секунда
    updateCoinDisplay();
    startPassiveIncome();
    alert('Пассивный доход улучшен!');
});

// Обработчики покупки геймпассов
gamepassButtons.forEach(button => {
    button.addEventListener('click', () => {
        const gamepass_key = button.getAttribute('data-key');
        const gamepass = gamepasses[gamepass_key];
        if (coins < gamepass.price) {
            alert('Недостаточно монет для покупки геймпасса.');
            return;
        }
        // Отправка запроса на сервер для покупки геймпасса
        fetch('https://fl8422.github.io/Fl8421.github.io/purchase_gamepass', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: user_id,
                gamepass_key: gamepass_key
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                coins -= gamepass.price;
                updateCoinDisplay();
                alert(data.message);
                button.classList.add('purchased');
                button.innerText = 'Куплено';
                button.disabled = true;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при покупке геймпасса.');
        });
    });
});

// Функция разблокировки игры
unlockButton.addEventListener('click', () => {
    const unlockCost = 65000;
    if (coins < unlockCost) {
        alert('Недостаточно монет для разблокировки игры.');
        return;
    }
    // Отправка запроса на сервер для разблокировки игры
    fetch('https://fl8422.github.io/Fl8421.github.io/unlock_clicker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: user_id
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            coins -= unlockCost;
            updateCoinDisplay();
            lockDiv.style.display = 'none';
            gameDiv.style.display = 'block';
            startPassiveIncome();
            alert('Игра успешно разблокирована!');
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при разблокировке игры.');
    });
});

// Инициализация геймпассов (можно загрузить из сервера)
const gamepasses = {
    'double_luck': {
        'name': 'Удвоение удачи',
        'price': 750000,
        'description': 'Удваивает удачу при добыче руды.'
    },
    'ultra_luck': {
        'name': 'Ультра удача',
        'price': 2500000,
        'description': 'Увеличивает удачу при добыче руды в 5 раз.'
    },
    'double_ore': {
        'name': 'Двойная руда',
        'price': 1000000,
        'description': 'Удваивает количество добываемой руды.'
    },
    'instant_smelting': {
        'name': 'Моментальная переплавка',
        'price': 1500000,
        'description': 'Позволяет переплавлять руду мгновенно без ожидания.'
    }
};

// Начальная настройка
updateCoinDisplay();
