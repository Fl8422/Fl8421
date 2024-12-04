document.getElementById('search-btn').addEventListener('click', performSearch);
const loader = document.getElementById('loader');
const results = document.getElementById('results');
const apiKey = 'AIzaSyBmjRNwNBNY1A6g6Qfv9aUBV_rD1Zz03lw'; // Укажите ваш ключ

function performSearch() {
    const query = document.getElementById('search-input').value;
    if (!query) return;

    loader.style.display = 'block';
    results.innerHTML = '';

    const url = `https://www.googleapis.com/customsearch/v1?q=${query}&key=${apiKey}&cx=YOUR_CX_CODE`; // Укажите код CX

    fetch(url)
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            const items = data.items || [];
            results.innerHTML = items
                .slice(0, Math.floor(Math.random() * 16) + 5) // Случайное число ссылок от 5 до 20
                .map(item => `<p><a href="${item.link}" target="_blank">${item.title}</a></p>`)
                .join('');
        })
        .catch(error => {
            loader.style.display = 'none';
            results.innerHTML = '<p>Произошла ошибка при выполнении поиска.</p>';
        });
}
