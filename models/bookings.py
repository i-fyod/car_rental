"""Бронирования: класс Booking и функции работы с List[Booking]."""
from typing import List, Optional

from utils import next_id, parse_date

from .cars import Car
from .clients import Client


class Booking:
    """Бронирование автомобиля клиентом на период [start, end]."""

    def __init__(
        self,
        booking_id: int,
        car: Car,
        start_date: str,
        end_date: str,
        client: Client,
    ) -> None:
        """Создать бронирование; конец периода не раньше начала."""
        if parse_date(end_date) < parse_date(start_date):
            raise ValueError("Дата окончания раньше даты начала.")
        self.id = booking_id
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.client = client
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить бронирование, не удаляя его из коллекции."""
        self.is_cancelled = True

    def days(self) -> int:
        """Число суток аренды, включая первый и последний день."""
        delta = parse_date(self.end_date) - parse_date(self.start_date)
        return delta.days + 1

    def total_price(self) -> int:
        """Стоимость аренды за весь период."""
        return self.days() * self.car.price_per_day

    def __str__(self) -> str:
        """Вернуть строковое представление бронирования."""
        state = "отменена" if self.is_cancelled else "активна"
        return (
            f"Бронь №{self.id}: {self.car.name}, "
            f"{self.start_date} – {self.end_date}, "
            f"{self.client.name} [{state}]"
        )


def find_booking_by_id(
    bookings: List[Booking],
    booking_id: int,
) -> Optional[Booking]:
    """Найти бронирование по идентификатору."""
    for booking in bookings:
        if booking.id == booking_id:
            return booking
    return None


def is_car_free_for_period(
    bookings: List[Booking],
    car: Car,
    start_date: str,
    end_date: str,
) -> bool:
    """Проверить, что нет активных броней автомобиля в этот период."""
    # ISO-даты сравниваются как строки; периоды пересекаются, если
    # начало одного не позже конца другого и наоборот.
    for booking in bookings:
        if booking.car.id != car.id or booking.is_cancelled:
            continue
        if booking.start_date <= end_date and start_date <= booking.end_date:
            return False
    return True


def is_car_available(
    bookings: List[Booking],
    car: Car,
    day: str,
) -> bool:
    """Проверить, свободен ли автомобиль в указанный день."""
    return is_car_free_for_period(bookings, car, day, day)


def create_booking(
    bookings: List[Booking],
    car: Car,
    start_date: str,
    end_date: str,
    client: Client,
) -> Optional[Booking]:
    """Создать бронь; вернуть None, если автомобиль занят в период."""
    if not is_car_free_for_period(bookings, car, start_date, end_date):
        return None
    booking = Booking(next_id(bookings), car, start_date, end_date, client)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: List[Booking], booking_id: int) -> bool:
    """Отменить бронь по идентификатору; False, если она не найдена."""
    booking = find_booking_by_id(bookings, booking_id)
    if booking is None:
        return False
    booking.cancel()
    return True


def get_booking_status(
    bookings: List[Booking],
    car: Car,
    day: str,
) -> str:
    """Сообщить о доступности автомобиля в указанный день."""
    if is_car_available(bookings, car, day):
        return f"{car.name} свободен {day}."
    return f"{car.name} занят {day}."


def show_bookings(bookings: List[Booking]) -> None:
    """Вывести список бронирований в консоль."""
    if not bookings:
        print("Бронирований нет.")
        return
    for booking in bookings:
        print(booking)
