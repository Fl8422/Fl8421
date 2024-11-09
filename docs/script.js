function performSearch() {
    const query = document.getElementById('searchInput').value;
    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('resultsContainer');
            resultsContainer.innerHTML = '';
            data.links.forEach(link => {
                const linkElement = document.createElement('div');
                linkElement.innerHTML = `<a href="${link}" target="_blank" style="color: white;">${link}</a>`;
                resultsContainer.appendChild(linkElement);
            });
        })
        .catch(error => console.error('Ошибка:', error));
}
