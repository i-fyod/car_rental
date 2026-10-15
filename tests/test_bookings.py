import pytest

from models import Booking
from models.bookings import (
    cancel_booking,
    create_booking,
    find_booking_by_id,
    get_booking_status,
    is_car_available,
    is_car_free_for_period,
)


def make_booking(cars, clients, start="2026-10-10", end="2026-10-12"):
    return Booking(1, cars[0], start, end, clients[0])


def test_booking_creation(cars, clients):
    booking = make_booking(cars, clients)

    assert booking.id == 1
    assert booking.car is cars[0]
    assert booking.client is clients[0]
    assert booking.start_date == "2026-10-10"
    assert booking.end_date == "2026-10-12"
    assert not booking.is_cancelled


def test_booking_rejects_reversed_period(cars, clients):
    with pytest.raises(ValueError):
        make_booking(cars, clients, "2026-10-12", "2026-10-10")


def test_booking_cancel(cars, clients):
    booking = make_booking(cars, clients)

    booking.cancel()

    assert booking.is_cancelled
    assert "отменена" in str(booking)


def test_booking_days_and_price(cars, clients):
    booking = make_booking(cars, clients)

    assert booking.days() == 3
    assert booking.total_price() == 3 * 4500


def test_car_availability(cars, clients):
    bookings = [make_booking(cars, clients)]

    assert not is_car_available(bookings, cars[0], "2026-10-10")
    assert not is_car_available(bookings, cars[0], "2026-10-12")
    assert is_car_available(bookings, cars[0], "2026-10-13")
    assert is_car_available(bookings, cars[1], "2026-10-11")


def test_period_overlap(cars, clients):
    bookings = [make_booking(cars, clients)]
    car = cars[0]

    assert not is_car_free_for_period(
        bookings, car, "2026-10-08", "2026-10-10")
    assert not is_car_free_for_period(
        bookings, car, "2026-10-11", "2026-10-20")
    assert not is_car_free_for_period(
        bookings, car, "2026-10-01", "2026-10-30")
    assert is_car_free_for_period(
        bookings, car, "2026-10-13", "2026-10-15")
    assert is_car_free_for_period(
        bookings, car, "2026-10-01", "2026-10-09")


def test_create_booking_adds_object(cars, clients):
    bookings = []

    booking = create_booking(
        bookings, cars[0], "2026-10-10", "2026-10-12", clients[0])

    assert booking is not None
    assert booking.car is cars[0]
    assert bookings == [booking]


def test_create_booking_rejects_busy_car(cars, clients):
    bookings = []
    create_booking(
        bookings, cars[0], "2026-10-10", "2026-10-12", clients[0])

    second = create_booking(
        bookings, cars[0], "2026-10-12", "2026-10-14", clients[1])

    assert second is None
    assert len(bookings) == 1


def test_cancelled_booking_does_not_block(cars, clients):
    bookings = []
    first = create_booking(
        bookings, cars[0], "2026-10-10", "2026-10-12", clients[0])
    first.cancel()

    second = create_booking(
        bookings, cars[0], "2026-10-10", "2026-10-12", clients[1])

    assert second is not None
    assert len(bookings) == 2


def test_cancel_booking_by_id(cars, clients):
    bookings = [make_booking(cars, clients)]

    assert cancel_booking(bookings, 1)
    assert bookings[0].is_cancelled
    assert not cancel_booking(bookings, 99)


def test_find_booking_by_id(cars, clients):
    bookings = [make_booking(cars, clients)]

    assert find_booking_by_id(bookings, 1) is bookings[0]
    assert find_booking_by_id(bookings, 2) is None


def test_get_booking_status(cars, clients):
    bookings = [make_booking(cars, clients)]

    assert "занят" in get_booking_status(bookings, cars[0], "2026-10-11")
    assert "свободен" in get_booking_status(bookings, cars[0], "2026-10-20")
