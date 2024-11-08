document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('query').value;
    if (query.trim() === "") {
        alert("Пожалуйста, введите запрос.");
        return;
    }

    fetch(`https://www.pythonanywhere.com/user/Fl8421/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = "";
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
            console.error('Ошибка:', error);
            alert("Произошла ошибка при поиске.");
        });
});
