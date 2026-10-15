import sqlite3
from contextlib import closing
from datetime import date

from django.shortcuts import render

from db.database import get_connection


def cars(request):
    """Список автомобилей из таблицы cars."""
    with closing(get_connection()) as conn:
        # Row позволяет обращаться к полям по имени: car.name в шаблоне.
        conn.row_factory = sqlite3.Row
        cars_list = conn.execute("""
            SELECT id, name, seats, car_type, price_per_day, description
            FROM cars
            ORDER BY name;
            """).fetchall()
    return render(request, "cars/car_list.html", {"cars": cars_list})


def car_detail(request, car_id):
    """Страница автомобиля с доступностью на сегодня."""
    available = None
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        car = conn.execute("""
            SELECT id, name, seats, car_type, price_per_day, description
            FROM cars
            WHERE id = ?;
            """, [car_id]).fetchone()
        if car is not None:
            busy = conn.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE car_id = ?
                  AND is_cancelled = 0
                  AND ? BETWEEN start_date AND end_date;
                """, [car_id, date.today().isoformat()]).fetchone()[0]
            available = busy == 0

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
