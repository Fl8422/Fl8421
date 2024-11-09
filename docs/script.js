// Обработчик события для кнопки "Поиск"
document.getElementById('search-button').addEventListener('click', function() {
  const query = document.getElementById('search-box').value.trim();
  if (query !== '') {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<p>Результаты поиска для "<strong>${query}</strong>":</p><ul></ul>`;
    const ul = resultsDiv.querySelector('ul');

    // Список поисковых систем
    const searchEngines = [
      { name: 'Google', url: 'https://www.google.com/search?q=' },
      { name: 'Bing', url: 'https://www.bing.com/search?q=' },
      { name: 'DuckDuckGo', url: 'https://duckduckgo.com/?q=' },
      { name: 'Yahoo', url: 'https://search.yahoo.com/search?p=' },
    ];

    // Определяем количество ссылок для отображения
    const minLinks = 3;
    const maxLinks = 20;
    let numberOfLinks = searchEngines.length;

    if (numberOfLinks < minLinks) {
      numberOfLinks = minLinks;
    } else if (numberOfLinks > maxLinks) {
      numberOfLinks = maxLinks;
    }

    // Генерируем ссылки на результаты поиска
    for (let i = 0; i < numberOfLinks; i++) {
      const engine = searchEngines[i % searchEngines.length]; // Зацикливаем список поисковых систем
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = engine.url + encodeURIComponent(query);
      a.target = '_blank';
      a.textContent = `Поиск в ${engine.name}`;
      li.appendChild(a);
      ul.appendChild(li);
    }
  } else {
    alert('Пожалуйста, введите запрос для поиска.');
  }
});
