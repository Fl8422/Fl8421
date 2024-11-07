let coins = 0;
let passiveIncome = 1;
let passiveIncomeLevel = 1;
let lastClickTime = 0;

// Получаем user_id через URL-параметры или другой метод
// Для примера, пусть user_id будет задан вручную
const user_id = prompt("Введите ваш Telegram ID для синхронизации:");

// Функция для обновления баланса на сервере
function updateBalanceOnServer() {
    fetch(`https://fl8422.github.io/Fl8421.github.io/api/get_balance?user_id=${user_id}`)
    .then(response => response.json())
    .then(data => {
        if(data.success){
            coins = data.balance;
            document.getElementById('coins').innerText = coins;
        }
    })
    .catch(error => {
        console.error('Ошибка при обновлении баланса:', error);
    });
}

// Функция для получения геймпассов
function getGamepasses() {
    fetch(`https://fl8422.github.io/Fl8421.github.io/api/get_gamepasses?user_id=${user_id}`)
    .then(response => response.json())
    .then(data => {
        if(data.success){
            data.gamepasses.forEach(gp => {
                if(gp === 'Удвоение удачи'){
                    passiveIncome *= 2;
                } else if(gp === 'Ультра удача'){
                    passiveIncome *= 5;
                } else if(gp === 'Двойная руда'){
                    // Реализуйте логику удвоения добычи, если требуется
                } else if(gp === 'Моментальная переплавка'){
                    // Реализуйте логику моментальной переплавки, если требуется
                }
            });
            document.getElementById('passive-income').innerText = `${passiveIncome} монета/${100 - (passiveIncomeLevel -1)} секунд`;
        }
    })
    .catch(error => {
        console.error('Ошибка при получении геймпассов:', error);
    });
}

// Инициализация игры
function initializeGame(){
    // Получаем баланс и геймпассы через API
    updateBalanceOnServer();
    getGamepasses();
}

// Обработчик кнопки разблокировки
document.getElementById('unlock-button').addEventListener('click', () => {
    fetch('https://fl8422.github.io/Fl8421.github.io/api/unlock_clicker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: parseInt(user_id) })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            document.getElementById('lock-container').style.display = 'none';
            document.getElementById('game-container').style.display = 'block';
            initializeGame();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});

// Обработчик кнопки клика
document.getElementById('click-button').addEventListener('click', () => {
    const currentTime = Date.now();
    if(currentTime - lastClickTime < 2000){
        alert("Вы можете кликать только раз в 2 секунды!");
        return;
    }
    lastClickTime = currentTime;
    coins += 1;
    document.getElementById('coins').innerText = coins;
    // Отправляем обновление баланса на сервер
    // Здесь можно реализовать API-запрос для обновления баланса на сервере
});

// Обработчик кнопки улучшения пассивного дохода
document.getElementById('upgrade-passive').addEventListener('click', () => {
    const upgradeCost = 7500 * passiveIncomeLevel;
    if(coins < upgradeCost){
        alert("У вас недостаточно монет для улучшения пассивного дохода.");
        return;
    }
    coins -= upgradeCost;
    passiveIncomeLevel += 1;
    passiveIncome += 1;
    document.getElementById('coins').innerText = coins;
    document.getElementById('passive-income').innerText = `${passiveIncome} монета/${100 - (passiveIncomeLevel -1)} секунд`;
    // Отправляем обновление пассивного дохода на сервер
    // Здесь можно реализовать API-запрос для обновления пассивного дохода на сервере
});

// Пассивный доход
setInterval(() => {
    coins += passiveIncome;
    document.getElementById('coins').innerText = coins;
    // Отправляем обновление баланса на сервер
    // Здесь можно реализовать API-запрос для обновления баланса на сервере
}, 100000); // 100 секунд
