document.getElementById('search-button').addEventListener('click', function() {
  const query = document.getElementById('search-box').value.trim();
  if (query !== '') {
    const url = `https://www.olx.ua/list/q-${encodeURIComponent(query)}/`;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
      <p>Результаты поиска для "<strong>${query}</strong>":</p>
      <ul>
        <li><a href="${url}" target="_blank">Посмотреть результаты на OLX.ua</a></li>
      </ul>
    `;
  } else {
    alert('Пожалуйста, введите запрос для поиска.');
  }
});
