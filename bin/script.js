async function performSearch(query) {
    try {
        const response = await fetch("http://localhost:5000/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
        });
        const results = await response.json();

        const resultsContainer = document.getElementById("resultsContainer");
        resultsContainer.innerHTML = "";
        results.forEach((link) => {
            const resultItem = document.createElement("p");
            resultItem.textContent = link;
            resultsContainer.appendChild(resultItem);
        });
    } catch (error) {
        console.error("Ошибка при выполнении поиска:", error);
    }
}

document.getElementById("searchButton").addEventListener("click", () => {
    const query = document.getElementById("searchInput").value;
    if (query) {
        performSearch(query);
    } else {
        alert("Введите запрос для поиска.");
    }
});
