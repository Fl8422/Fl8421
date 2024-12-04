// Конфигурация API
const apiKey = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw'; // Укажите ваш Google API Key
const engineId = '1277afbc49d06402d'; // Укажите ваш Search Engine ID

// Элементы DOM
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const dropdownBtn = document.getElementById('dropdown-btn');
const dropdownOptions = document.querySelectorAll('.search-option');
const loader = document.getElementById('loader');
const results = document.getElementById('results');

// Тип поиска (по умолчанию: стандартный)
let searchType = 'standard';

// Обновление типа поиска
dropdownOptions.forEach(option => {
    option.addEventListener('click', () => {
        searchType = option.getAttribute('data-type');
        dropdownBtn.textContent = `Тип поиска: ${option.textContent}`;
    });
});

// Обработчик поиска
searchBtn.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (!query) return;

    loader.style.display = 'block';
    results.innerHTML = '';

    // Формирование URL для разных типов поиска
    let url = `https://www.googleapis.com/customsearch/v1?q=${query}&key=${apiKey}&cx=${engineId}`;
    if (searchType === 'time') {
        url += '&sort=date'; // Поиск по времени
    } else if (searchType === 'site') {
        const site = prompt('Введите сайт (например, example.com):');
        if (site) url += ` site:${site}`; // Поиск по сайту
    }

    // Выполнение запроса
    fetch(url)
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            const items = data.items || [];
            results.innerHTML = items
                .slice(0, Math.floor(Math.random() * 16) + 5) // Случайное количество ссылок (от 5 до 20)
                .map(item => `<p><a href="${item.link}" target="_blank">${item.title}</a></p>`)
                .join('');
        })
        .catch(error => {
            loader.style.display = 'none';
            results.innerHTML = '<p>Ошибка при выполнении поиска. Проверьте API Key и Engine ID.</p>';
        });
});
