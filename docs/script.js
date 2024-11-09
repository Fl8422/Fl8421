function performSearch() {
    const query = document.getElementById('search-box').value;
    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsList = document.getElementById('results-list');
            resultsList.innerHTML = '';
            data.links.forEach(link => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<a href="${link}" target="_blank">${link}</a>`;
                resultsList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Ошибка:', error));
}
