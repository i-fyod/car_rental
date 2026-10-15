from datetime import date

from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.bookings import is_car_available
from models.cars import find_car_by_id
from storage import load_all


def cars(request):
    """Список автомобилей."""
    cars_list, _, _ = load_all()
    items = ""
    for car in cars_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/cars/{car.id}/">{escape(car.name)}</a>
            <span>
                {escape(car.car_type)}, {car.seats} мест,
                {car.price_per_day} руб./сутки
            </span>
        </li>
        """
    content = f"""
    <h1>Автомобили</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Автомобили", content))


def car_detail(request, car_id):
    """Страница автомобиля с доступностью на сегодня."""
    cars_list, _, bookings_list = load_all()
    car = find_car_by_id(cars_list, car_id)

    if car is None:
        content = """
        <h1 class="text-danger">Автомобиль не найден</h1>
        <a href="/cars/" class="btn btn-outline-secondary">
            ← к списку автомобилей
        </a>
        """
        return HttpResponse(
            page("Автомобиль не найден", content),
            status=404,
        )

    available = is_car_available(bookings_list, car, date.today().isoformat())
    status = "свободен" if available else "занят"
    badge = "bg-success" if available else "bg-danger"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(car.name)}</h5>
            <p class="card-text"><strong>ID:</strong> {car.id}</p>
            <p class="card-text">
                <strong>Тип кузова:</strong> {escape(car.car_type)}
            </p>
            <p class="card-text">
                <strong>Мест:</strong> {car.seats}
            </p>
            <p class="card-text">
                <strong>Цена:</strong> {car.price_per_day} руб./сутки
            </p>
            <p class="card-text">{escape(car.description)}</p>
            <p class="card-text">
                Сегодня:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/cars/" class="btn btn-outline-secondary">
                ← к списку автомобилей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(car.name, content))
