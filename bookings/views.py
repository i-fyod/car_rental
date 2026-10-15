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
