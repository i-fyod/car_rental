from django.http import HttpResponse
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
    """Главная страница с описанием сервиса и навигацией."""
    content = """
    <h1 class="display-4">Прокат автомобилей</h1>
    <p class="lead">Сервис аренды автомобилей.</p>
    <p>Основные разделы:</p>
    <a href="/cars/" class="btn btn-primary me-2">Автомобили</a>
    <a href="/bookings/" class="btn btn-secondary">Бронирования</a>
    """
    return HttpResponse(page("Прокат автомобилей", content))


def page_not_found(request, exception):
    """Страница 404 для любого адреса без маршрута."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
