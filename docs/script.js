document.getElementById('search-button').addEventListener('click', function() {
  const query = document.getElementById('search-box').value;
  const url = `https://www.olx.ua/list/q-${encodeURIComponent(query)}/`;
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = `<a href="${url}" target="_blank">Посмотреть результаты поиска на OLX.ua</a>`;
});
