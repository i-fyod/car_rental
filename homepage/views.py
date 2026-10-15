from django.shortcuts import render


def index(request):
    """Главная страница: шаблон без динамических данных."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Страница 404 для любого адреса без маршрута."""
    return render(request, "homepage/404.html", status=404)
