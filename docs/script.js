let coinCount = 0;
let passiveIncome = 1; // Монет в 100 секунд
let passiveInterval = null;

// Функция для обновления отображения монет
function updateCoinDisplay() {
    document.getElementById('coin-count').innerText = coinCount;
    document.getElementById('passive-income').innerText = passiveIncome;
}

// Функция для пассивного дохода
function startPassiveIncome() {
    if (passiveInterval) clearInterval(passiveInterval);
    passiveInterval = setInterval(() => {
        coinCount += passiveIncome;
        updateCoinDisplay();
        // Отправка обновления в Telegram бот через API
        sendCoinUpdate();
    }, 100000); // 100 секунд
}

// Функция для клика
document.getElementById('clicker-button').addEventListener('click', () => {
    const now = Date.now();
    if (now - (window.lastClick || 0) < 2000) { // 2 секунды
        alert("Вы кликаете слишком часто! Подождите немного.");
        return;
    }
    window.lastClick = now;
    coinCount += 1;
    updateCoinDisplay();
    sendCoinUpdate();
});

// Функция для улучшения пассивного дохода
document.getElementById('upgrade-passive').addEventListener('click', () => {
    if (coinCount >= 7500) {
        coinCount -= 7500;
        passiveIncome += 1;
        updateCoinDisplay();
        startPassiveIncome();
        sendCoinUpdate();
    } else {
        alert("У вас недостаточно монет для улучшения пассивного дохода.");
    }
});

// Функция для покупки геймпассов
document.querySelectorAll('.buy-button').forEach(button => {
    button.addEventListener('click', () => {
        const gamePassDiv = button.parentElement;
        const gamePassId = gamePassDiv.id;
        // Отправка запроса на покупку геймпасса через Telegram бот API
        buyGamePass(gamePassId, button);
    });
});

// Функция для покупки геймпасса
function buyGamePass(passType, button) {
    fetch('https://fl8422.github.io/Fl8421.github.io/buy_game_pass', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ passType: passType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Вы купили геймпасс '${data.passName}'.`);
            button.classList.add('purchased');
            button.innerText = 'Куплено';
            // Применение эффекта геймпасса
            applyGamePass(data.passType);
        } else {
            alert(`Ошибка: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Ошибка при покупке геймпасса:', error);
    });
}

// Функция для применения геймпассов
function applyGamePass(passType) {
    if (passType === 'double_luck') {
        // Удвоение удачи: увеличить шанс на более ценные руды
        // Реализация зависит от серверной части игры
    }
    if (passType === 'ultra_luck') {
        // Ультра удача: увеличить шанс на еще более ценные руды
    }
    if (passType === 'double_ore') {
        // Двойная руда: удваивает добываемую руду
        coinCount *= 2;
        updateCoinDisplay();
    }
    if (passType === 'instant_smelting') {
        // Моментальная переплавка: убрать время ожидания
        // Реализация зависит от серверной части игры
    }
}

// Функция для отправки обновления монет в Telegram бот
function sendCoinUpdate() {
    fetch('https://fl8422.github.io/Fl8421.github.io/update_coins', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coins: coinCount })
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа от сервера
    })
    .catch(error => {
        console.error('Ошибка при отправке обновления монет:', error);
    });
}

// Запуск пассивного дохода при загрузке страницы
startPassiveIncome();
