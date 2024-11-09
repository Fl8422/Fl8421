async function performSearch(query) {
  
  const url = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${cx}&q=${encodeURIComponent(query)}`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    displayResults(data.items);
  } catch (error) {
    console.error('Ошибка при выполнении запроса:', error);
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<p>Ошибка при выполнении запроса: ${error.message}</p>`;
  }
}

function displayResults(items) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (items && items.length > 0) {
    items.slice(0, 4).forEach(item => {
      const resultItem = document.createElement('div');
      resultItem.style.marginBottom = '20px';

      const title = document.createElement('a');
      title.href = item.link;
      title.textContent = item.title;
      title.target = '_blank';
      title.style.display = 'block';

      const snippet = document.createElement('p');
      snippet.textContent = item.snippet;

      resultItem.appendChild(title);
      resultItem.appendChild(snippet);
      resultsDiv.appendChild(resultItem);
    });
  } else {
    resultsDiv.textContent = 'Нет результатов.';
  }
}

document.getElementById('search-button').addEventListener('click', function() {
  const query = document.getElementById('search-box').value.trim();
  if (query !== '') {
    performSearch(query);
  } else {
    alert('Пожалуйста, введите запрос для поиска.');
  }
});
