document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('links-container');
        container.innerHTML = '';
        data.links.forEach(link => {
            const linkDiv = document.createElement('div');
            linkDiv.className = 'link-item';
            linkDiv.textContent = link;
            container.appendChild(linkDiv);
        });
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});
