let searchType = 'standard';

function toggleDropdown() {
    const menu = document.getElementById('dropdownMenu');
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

function setSearchType(type) {
    searchType = type;
    document.getElementById('dropdownMenu').style.display = 'none';
}

document.getElementById('searchButton').addEventListener('click', function() {
    const query = document.getElementById('searchQuery').value;
    if (query) {
        document.getElementById('loading').style.display = 'block';
        fetch(`/search?query=${query}&type=${searchType}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                const resultsBox = document.getElementById('results');
                resultsBox.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(item => {
                        const link = document.createElement('a');
                        link.href = item.link;
                        link.textContent = item.title;
                        link.target = '_blank';
                        resultsBox.appendChild(link);
                        resultsBox.appendChild(document.createElement('br'));
                    });
                } else {
                    resultsBox.textContent = 'Не найдено результатов.';
                }
            });
    }
});
