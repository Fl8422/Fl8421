// Укажите свои ключи
const apiKey = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw';
const engineId = '1277afbc49d06402d';

// DOM элементы
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const dropdownBtn = document.getElementById('dropdown-btn');
const dropdownOptions = document.querySelectorAll('.search-option');
const loader = document.getElementById('loader');
const results = document.getElementById('results');

// Тип поиска
let searchType = 'standard';

// Изменение типа поиска
dropdownOptions.forEach(option => {
    option.addEventListener('click', () => {
        searchType = option.getAttribute('data-type');
        dropdownBtn.textContent = `Тип поиска: ${option.textContent}`;
    });
});

// Выполнение поиска
searchBtn.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (!query) return;

    loader.style.display = 'block';
    results.innerHTML = '';

    let url = `https://www.googleapis.com/customsearch/v1?q=${query}&key=${apiKey}&cx=${engineId}`;

    // Обработка разных типов поиска
    if (searchType === 'detailed') {
        url += '&fields=items(title,link,snippet)';
    } else if (searchType === 'time') {
        url += '&sort=date';
    } else if (searchType === 'site') {
        const site = prompt('Введите сайт (например, example.com):');
        if (site) url += `+site:${site}`;
    }

    // Отправка запроса
    fetch(url)
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            if (data.items) {
                results.innerHTML = data.items
                    .map(item => `<p><a href="${item.link}" target="_blank">${item.title}</a></p>`)
                    .join('');
            } else {
                results.innerHTML = '<p>Ничего не найдено.</p>';
            }
        })
        .catch(error => {
            loader.style.display = 'none';
            results.innerHTML = `<p>Ошибка: ${error.message}</p>`;
        });
});
