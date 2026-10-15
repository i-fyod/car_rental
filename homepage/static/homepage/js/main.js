// Подставляет текущий год в подвал страницы.
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Подсвечивает пункт меню, соответствующий текущему адресу.
document.querySelectorAll(".site-nav a").forEach(function (link) {
    const path = link.getAttribute("href");
    const current = window.location.pathname;
    const isActive = path === "/" ? current === "/" : current.startsWith(path);

    if (isActive) {
        link.classList.add("active");
    }
});
