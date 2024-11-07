const tg = window.Telegram.WebApp;

// Функция покупки геймпасса
function buyPass(passType) {
    // Отправляем данные о покупке боту
    const data = { pass_type: passType };
    tg.sendData(JSON.stringify(data));

    // На время ожидания ответа от бота делаем кнопку неактивной
    const button = document.querySelector(`#${passType} .buy-button`);
    button.disabled = true;
    button.innerText = 'Покупка...';
    button.style.backgroundColor = '#ffa500'; // Темно-оранжевый цвет
}

// Функция для обновления состояния кнопки после покупки
function updateButton(passType, status) {
    const button = document.querySelector(`#${passType} .buy-button`);
    if (status === 'success') {
        button.classList.add('purchased');
        button.innerText = 'Куплено';
        button.style.backgroundColor = 'green';
        button.disabled = true;
    } else {
        button.disabled = false;
        button.innerText = 'Купить';
        button.style.backgroundColor = 'orange';
        alert('Покупка не удалась. Попробуйте снова.');
    }
}

// Обработка события получения данных от бота
tg.onEvent('data', function(data) {
    try {
        const response = JSON.parse(data);
        if (response.pass_type && response.status) {
            updateButton(response.pass_type, response.status);
        }
    } catch (error) {
        console.error('Ошибка обработки ответа:', error);
    }
});

// Функция для получения списка купленных пассов при загрузке
function getPurchasedPasses() {
    // Здесь вы можете реализовать запрос к вашему боту для получения списка купленных пассов
    // Для упрощения предположим, что список пассов передаётся через WebApp initialization data
    // Например, tg.initDataUnsafe.query_id может использоваться для запросов
}

tg.ready(() => {
    getPurchasedPasses();
});
