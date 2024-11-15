// Режим поиска (по умолчанию стандартный)
let searchMode = 'standard';

// Установить режим поиска
function setMode(mode) {
    searchMode = mode;
    console.log(`Выбран режим: ${searchMode}`);
}

// Обработка кнопки "Поиск"
document.getElementById('search-button').addEventListener('click', () => {
    const query = document.getElementById('search-input').value.trim();
    if (!query) {
        alert('Введите запрос!');
        return;
    }

    // Выполнить поиск
    performSearch(query);
});

// Выполнение поиска
async function performSearch(query) {
    // Укажите ваш API-ключ Google и идентификатор поискового движка
    const API_KEY = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw';
    const CX = '1277afbc49d06402d';

    // URL для API-запроса
    const url = `https://www.googleapis.com/customsearch/v1?q=${encodeURIComponent(query)}&key=${API_KEY}&cx=${CX}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        // Обработать результаты
        displayResults(data.items || []);
    } catch (error) {
        console.error('Ошибка выполнения поиска:', error);
        alert('Ошибка выполнения поиска!');
    }
}

// Отображение результатов
function displayResults(items) {
    const resultsBox = document.getElementById('results-box');
    resultsBox.innerHTML = ''; // Очистить старые результаты

    if (items.length === 0) {
        resultsBox.innerHTML = '<p>Ничего не найдено.</p>';
        return;
    }

    // Добавить результаты в блок
    items.forEach((item) => {
        const link = document.createElement('a');
        link.href = item.link;
        link.textContent = item.title || item.link;
        link.target = '_blank';
        link.style.display = 'block';
        link.style.marginBottom = '10px';

        resultsBox.appendChild(link);
    });
}
