"""Загрузка и сохранение данных в JSON."""
import json
from pathlib import Path
from typing import Any, List

from models import Booking, Car, Client
from models.cars import find_car_by_id
from models.clients import find_client_by_id

CARS_PATH = "data/cars.json"
CLIENTS_PATH = "data/clients.json"
BOOKINGS_PATH = "data/bookings.json"


def _read_json(path: str) -> List[Any]:
    """Прочитать список из JSON-файла; пустой список, если файла нет."""
    file = Path(path)
    if not file.exists():
        return []
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Файл {path} повреждён: {error}") from error


def _write_json(path: str, items: List[Any]) -> None:
    """Записать список в JSON-файл, создав каталог при необходимости."""
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(
        json.dumps(items, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def load_cars(path: str = CARS_PATH) -> List[Car]:
    """Загрузить автомобили из JSON в список объектов Car."""
    return [Car.from_data(item) for item in _read_json(path)]


def save_cars(cars: List[Car], path: str = CARS_PATH) -> None:
    """Сохранить автомобили в JSON."""
    _write_json(path, [
        {
            "id": car.id,
            "name": car.name,
            "seats": car.seats,
            "car_type": car.car_type,
            "price_per_day": car.price_per_day,
            "description": car.description,
        }
        for car in cars
    ])


def load_clients(path: str = CLIENTS_PATH) -> List[Client]:
    """Загрузить клиентов из JSON в список объектов Client."""
    return [Client.from_data(item) for item in _read_json(path)]


def save_clients(clients: List[Client], path: str = CLIENTS_PATH) -> None:
    """Сохранить клиентов в JSON."""
    _write_json(path, [
        {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
        }
        for client in clients
    ])


def load_bookings(
    path: str,
    cars: List[Car],
    clients: List[Client],
) -> List[Booking]:
    """Загрузить брони и восстановить связи с автомобилями и клиентами."""
    bookings: List[Booking] = []
    for item in _read_json(path):
        car = find_car_by_id(cars, item["car_id"])
        client = find_client_by_id(clients, item["client_id"])
        if car is None or client is None:
            raise ValueError(
                f"Бронь {item['id']}: не найден автомобиль или клиент."
            )
        booking = Booking(
            item["id"], car, item["start_date"], item["end_date"], client,
        )
        booking.is_cancelled = item["is_cancelled"]
        bookings.append(booking)
    return bookings


def save_bookings(
    bookings: List[Booking],
    path: str = BOOKINGS_PATH,
) -> None:
    """Сохранить брони в JSON, заменив объекты их идентификаторами."""
    _write_json(path, [
        {
            "id": booking.id,
            "car_id": booking.car.id,
            "client_id": booking.client.id,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "is_cancelled": booking.is_cancelled,
        }
        for booking in bookings
    ])
