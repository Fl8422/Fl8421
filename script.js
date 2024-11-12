document.getElementById("seo-panel").addEventListener("click", function() {
    document.querySelector(".title").textContent = "SEO Panel";
    document.getElementById("seo-panel").classList.add("active");
    document.getElementById("osint-panel").classList.remove("active");
});

document.getElementById("osint-panel").addEventListener("click", function() {
    document.querySelector(".title").textContent = "OSINT Panel";
    document.getElementById("osint-panel").classList.add("active");
    document.getElementById("seo-panel").classList.remove("active");
});
