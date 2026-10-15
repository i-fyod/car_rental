from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import escape


def page(title, content):
    """Собрать HTML-страницу: каркас, Bootstrap и навигацию."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/cars/">Автомобили</a>
        <a class="nav-link" href="/bookings/">Бронирования</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: шаблон без динамических данных."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Страница 404 для любого адреса без маршрута."""
    return render(request, "homepage/404.html", status=404)
