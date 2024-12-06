let searchType = 'standard';

function setSearchType(type) {
  searchType = type;
  document.getElementById('searchTypeBtn').innerText = type === 'standard' ? 'Стандартный поиск' :
    type === 'detailed' ? 'Подробный поиск' :
    type === 'time' ? 'Поиск по времени' : 'Поиск по сайту';
}

function performSearch() {
  const query = document.getElementById('searchInput').value;
  if (!query) {
    alert('Введите запрос!');
    return;
  }
  
  // Очистка предыдущих результатов и отображение индикатора загрузки
  document.getElementById('results').innerHTML = '';
  document.getElementById('loading').style.display = 'block';

  let cx = '1277afbc49d06402d';  // Укажите свой Engine ID
  let apiKey = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw';  // Укажите свой Google API Key
  let searchUrl = `https://www.googleapis.com/customsearch/v1?q=${query}&key=${apiKey}&cx=${cx}`;

  // Различные параметры поиска в зависимости от типа
  if (searchType === 'time') {
    // Поиск за последнюю неделю
    const date = new Date();
    date.setDate(date.getDate() - 7);
    const timeFilter = date.toISOString().split('T')[0]; // Формат YYYY-MM-DD
    searchUrl += `&dateRestrict=w${timeFilter}`;
  } else if (searchType === 'site') {
    // Поиск по конкретному сайту (например, site:example.com)
    searchUrl += `&siteSearch=${query}`;
  }

  // Для подробного поиска: добавление параметра для извлечения текста (например, расширенный поиск с описанием)
  let detailedSearch = searchType === 'detailed' ? '&fields=items(title,link,snippet)' : '';
  searchUrl += detailedSearch;

  // Выполнение запроса
  fetch(searchUrl)
    .then(response => response.json())
    .then(data => {
      document.getElementById('loading').style.display = 'none';
      if (data.items) {
        data.items.forEach(item => {
          const resultElement = document.createElement('div');
          resultElement.classList.add('result-item');
          resultElement.innerHTML = `<a href="${item.link}" target="_blank">${item.title}</a><p>${item.snippet}</p>`;
          document.getElementById('results').appendChild(resultElement);
        });
      } else {
        document.getElementById('results').innerHTML = 'Ничего не найдено.';
      }
    })
    .catch(error => {
      document.getElementById('loading').style.display = 'none';
      document.getElementById('results').innerHTML = 'Ошибка поиска.';
    });
}

// Плавное раскрытие меню поиска
document.getElementById('searchTypeBtn').addEventListener('click', function() {
  const dropdownContent = document.querySelector('.dropdown-content');
  dropdownContent.classList.toggle('show');
});

// Закрытие меню при выборе элемента
const links = document.querySelectorAll('.dropdown-content a');
links.forEach(link => {
  link.addEventListener('click', function() {
    const dropdownContent = document.querySelector('.dropdown-content');
    dropdownContent.classList.remove('show');
  });
});
