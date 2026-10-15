from datetime import date

from django.shortcuts import render

from models.bookings import is_car_available
from models.cars import find_car_by_id
from storage import load_all


def cars(request):
    """Список автомобилей."""
    cars_list, _, _ = load_all()
    context = {
        "cars": cars_list,
    }
    return render(request, "cars/car_list.html", context)


def car_detail(request, car_id):
    """Страница автомобиля с доступностью на сегодня."""
    cars_list, _, bookings_list = load_all()
    car = find_car_by_id(cars_list, car_id)

    available = None
    if car is not None:
        today = date.today().isoformat()
        available = is_car_available(bookings_list, car, today)

    context = {
        "car": car,
        "available": available,
    }
    return render(
        request,
        "cars/car_detail.html",
        context,
        status=404 if car is None else 200,
    )
