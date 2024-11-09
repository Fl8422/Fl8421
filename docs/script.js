document.addEventListener('DOMContentLoaded', function() {
    // Переключение вкладок
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Удаляем активный класс у всех кнопок
            tabButtons.forEach(btn => btn.classList.remove('active'));
            // Добавляем активный класс на текущую кнопку
            button.classList.add('active');

            // Скрываем все вкладки
            tabContents.forEach(content => content.classList.remove('active'));
            // Показываем выбранную вкладку
            const activeTab = document.getElementById(button.getAttribute('data-tab'));
            activeTab.classList.add('active');
        });
    });

    // Обработчик поиска для Parser
    document.getElementById('search-button').addEventListener('click', function() {
        const query = document.getElementById('parser-query').value;
        if (query.trim() === "") {
            alert("Пожалуйста, введите запрос.");
            return;
        }

        // Отправка запроса на сервер
        fetch(`https://your-pythonanywhere-username.pythonanywhere.com/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('parser-results');
                resultsDiv.innerHTML = "";
                if (data.links.length === 0) {
                    resultsDiv.innerHTML = "<p>Ничего не найдено.</p>";
                    return;
                }
                data.links.forEach(link => {
                    const div = document.createElement('div');
                    div.className = 'result-item';
                    div.innerHTML = `<p><a href="${link}" target="_blank">${link}</a></p>`;
                    resultsDiv.appendChild(div);
                });
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert("Произошла ошибка при поиске.");
            });
    });

    // Обработчик поиска для Глаз бога
    document.getElementById('glaz-search-button').addEventListener('click', function() {
        const query = document.getElementById('glaz-query').value;
        if (query.trim() === "") {
            alert("Пожалуйста, введите информацию для поиска.");
            return;
        }

        // Получаем выбранные типы поиска
        const selectedTypes = Array.from(document.querySelectorAll('input[name="search-type"]:checked')).map(input => input.value);
        if (selectedTypes.length === 0) {
            alert("Пожалуйста, выберите хотя бы один тип поиска.");
            return;
        }

        // Отправка запроса на сервер
        fetch(`https://your-pythonanywhere-username.pythonanywhere.com/glaz-boga-search?q=${encodeURIComponent(query)}&types=${selectedTypes.join(',')}`)
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('glaz-results');
                resultsDiv.innerHTML = "";
                if (Object.keys(data.results).length === 0) {
                    resultsDiv.innerHTML = "<p>Ничего не найдено.</p>";
                    return;
                }

                for (const [category, results] of Object.entries(data.results)) {
                    const categoryDiv = document.createElement('div');
                    categoryDiv.className = 'result-category';
                    const categoryTitle = document.createElement('h3');
                    categoryTitle.textContent = capitalizeFirstLetter(category);
                    categoryDiv.appendChild(categoryTitle);

                    for (const [key, value] of Object.entries(results)) {
                        const p = document.createElement('p');
                        p.innerHTML = `<strong>${capitalizeFirstLetter(key.replace('_', ' '))}:</strong> ${value || 'Не найдено'}`;
                        categoryDiv.appendChild(p);
                    }

                    resultsDiv.appendChild(categoryDiv);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert("Произошла ошибка при поиске.");
            });
    });

    // Функция для капитализации первой буквы
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
});
