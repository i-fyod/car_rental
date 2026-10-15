import sqlite3
from contextlib import closing

from django.shortcuts import render

from db.database import get_connection


def bookings(request):
    """Список бронирований с автомобилем и клиентом (JOIN трёх таблиц)."""
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        bookings_list = conn.execute("""
            SELECT
                bookings.id,
                bookings.start_date,
                bookings.end_date,
                bookings.is_cancelled,
                cars.name AS car_name,
                clients.name AS client_name
            FROM bookings
            JOIN cars
                ON bookings.car_id = cars.id
            JOIN clients
                ON bookings.client_id = clients.id
            ORDER BY bookings.start_date;
            """).fetchall()
    return render(
        request,
        "bookings/booking_list.html",
        {"bookings": bookings_list},
    )


def booking_detail(request, booking_id):
    """Страница бронирования: срок и стоимость считает SQL."""
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        # Суток аренды: разность дат в днях плюс первый день.
        booking = conn.execute("""
            SELECT
                bookings.id,
                bookings.car_id,
                bookings.start_date,
                bookings.end_date,
                bookings.is_cancelled,
                cars.name AS car_name,
                clients.name AS client_name,
                CAST(julianday(bookings.end_date)
                     - julianday(bookings.start_date) AS INTEGER) + 1
                    AS days,
                cars.price_per_day
                * (CAST(julianday(bookings.end_date)
                        - julianday(bookings.start_date) AS INTEGER) + 1)
                    AS total_price
            FROM bookings
            JOIN cars
                ON bookings.car_id = cars.id
            JOIN clients
                ON bookings.client_id = clients.id
            WHERE bookings.id = ?;
            """, [booking_id]).fetchone()

    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
        status=404 if booking is None else 200,
    )


def statistics(request):
    """Статистика: брони по автомобилям, выручка и популярные машины."""
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        per_car = conn.execute("""
            SELECT
                cars.name AS car_name,
                COUNT(bookings.id) AS bookings_count
            FROM cars
            LEFT JOIN bookings
                ON cars.id = bookings.car_id
                AND bookings.is_cancelled = 0
            GROUP BY cars.id, cars.name
            ORDER BY bookings_count DESC, cars.name;
            """).fetchall()
        revenue = conn.execute("""
            SELECT
                cars.car_type,
                COUNT(bookings.id) AS bookings_count,
                SUM(
                    cars.price_per_day
                    * (CAST(julianday(bookings.end_date)
                            - julianday(bookings.start_date) AS INTEGER)
                       + 1)
                ) AS revenue
            FROM bookings
            JOIN cars
                ON bookings.car_id = cars.id
            WHERE bookings.is_cancelled = 0
            GROUP BY cars.car_type
            ORDER BY revenue DESC;
            """).fetchall()
        popular = conn.execute("""
            SELECT
                cars.name AS car_name,
                COUNT(bookings.id) AS bookings_count
            FROM cars
            JOIN bookings
                ON cars.id = bookings.car_id
            WHERE bookings.is_cancelled = 0
            GROUP BY cars.id, cars.name
            HAVING COUNT(bookings.id) >= 2
            ORDER BY bookings_count DESC, cars.name;
            """).fetchall()

    context = {
        "per_car": per_car,
        "revenue": revenue,
        "popular": popular,
    }
    return render(request, "bookings/statistics.html", context)
