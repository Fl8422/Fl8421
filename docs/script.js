document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('query').value.trim();
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');

    if (query === "") {
        alert("Пожалуйста, введите запрос.");
        return;
    }

    // Показываем загрузчик и очищаем предыдущие результаты
    loader.style.display = 'block';
    resultsDiv.innerHTML = "";

    // Замените 'your_username' на ваш реальный логин на PythonAnywhere
    const apiUrl = `https://your_username.pythonanywhere.com/search?q=${encodeURIComponent(query)}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            if (data.links && data.links.length > 0) {
                data.links.forEach(link => {
                    const div = document.createElement('div');
                    div.className = 'result-item';
                    div.innerHTML = `<a href="${link}" target="_blank">${link}</a>`;
                    resultsDiv.appendChild(div);
                });
            } else {
                resultsDiv.innerHTML = "<p>Ничего не найдено.</p>";
            }
        })
        .catch(error => {
            loader.style.display = 'none';
            console.error('Ошибка:', error);
            alert("Произошла ошибка при поиске.");
        });
});
