document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('query').value;
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');

    if (query.trim() === "") {
        alert("Пожалуйста, введите запрос.");
        return;
    }

    // Показываем загрузчик и очищаем предыдущие результаты
    loader.style.display = 'block';
    resultsDiv.innerHTML = "";

    fetch(`https://your-pythonanywhere-username.pythonanywhere.com/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            if (data.links.length === 0) {
                resultsDiv.innerHTML = "<p>Ничего не найдено.</p>";
                return;
            }
            data.links.forEach(link => {
                const div = document.createElement('div');
                div.className = 'result-item';
                div.innerHTML = `<a href="${link}" target="_blank">${link}</a>`;
                resultsDiv.appendChild(div);
            });
        })
        .catch(error => {
            loader.style.display = 'none';
            console.error('Ошибка:', error);
            alert("Произошла ошибка при поиске.");
        });
});
