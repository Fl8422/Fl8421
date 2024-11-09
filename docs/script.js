document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value.trim();
    if (query === "") {
        alert("Пожалуйста, введите поисковый запрос.");
        return;
    }

    // Очистка предыдущих результатов
    const container = document.getElementById('links-container');
    container.innerHTML = '<p>Загрузка...</p>';

    fetch('/search', { // Убедитесь, что эндпоинт '/search' настроен правильно
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        container.innerHTML = ''; // Очистка контейнера

        if (data.error) {
            container.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        if (data.links.length === 0) {
            container.innerHTML = '<p>Нет результатов.</p>';
            return;
        }

        data.links.forEach(link => {
            const linkDiv = document.createElement('div');
            linkDiv.className = 'link-item';

            const linkElement = document.createElement('a');
            linkElement.href = link;
            linkElement.textContent = link;
            linkElement.target = '_blank';
            linkElement.style.color = '#FFA500';
            linkElement.style.textDecoration = 'none';
            linkElement.style.wordBreak = 'break-all';

            linkDiv.appendChild(linkElement);
            container.appendChild(linkDiv);
        });
    })
    .catch(error => {
        console.error('Ошибка:', error);
        container.innerHTML = '<p>Произошла ошибка при поиске.</p>';
    });
});

// Дополнительная функциональность: обработка нажатия Enter в поле ввода
document.getElementById('search-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        document.getElementById('search-button').click();
    }
});
