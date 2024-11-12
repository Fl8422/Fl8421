async function performSearch() {
    const query = document.getElementById("query").value;
    document.getElementById("results").innerHTML = "Идет поиск...";
    try {
        const response = await fetch(`https://www.pythonanywhere.com/user/Fl8421/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        displayResults(data.results);
    } catch (error) {
        document.getElementById("results").innerHTML = "Ошибка поиска.";
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";
    results.forEach(link => {
        const linkElement = document.createElement("a");
        linkElement.href = link;
        linkElement.textContent = link;
        linkElement.target = "_blank";
        linkElement.style.display = "block";
        linkElement.style.color = "#FFA500";
        resultsDiv.appendChild(linkElement);
    });
}
