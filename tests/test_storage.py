import json

import pytest

from models import Booking
from storage import (
    load_bookings,
    load_cars,
    load_clients,
    save_bookings,
    save_cars,
    save_clients,
)


def test_load_missing_file_returns_empty(tmp_path):
    assert load_cars(str(tmp_path / "none.json")) == []
    assert load_clients(str(tmp_path / "none.json")) == []


def test_cars_roundtrip(tmp_path, cars):
    path = str(tmp_path / "cars.json")

    save_cars(cars, path)
    loaded = load_cars(path)

    assert [c.name for c in loaded] == [c.name for c in cars]
    assert loaded[1].seats == 9


def test_clients_roundtrip(tmp_path, clients):
    path = str(tmp_path / "clients.json")

    save_clients(clients, path)
    loaded = load_clients(path)

    assert [c.email for c in loaded] == [c.email for c in clients]


def test_bookings_roundtrip_restores_links(tmp_path, cars, clients):
    path = str(tmp_path / "bookings.json")
    booking = Booking(1, cars[1], "2026-10-10", "2026-10-12", clients[0])
    booking.cancel()

    save_bookings([booking], path)
    data = json.loads((tmp_path / "bookings.json").read_text("utf-8"))
    loaded = load_bookings(path, cars, clients)

    assert data[0]["car_id"] == 2
    assert data[0]["client_id"] == 1
    assert loaded[0].car is cars[1]
    assert loaded[0].client is clients[0]
    assert loaded[0].is_cancelled


def test_load_bookings_unknown_car_raises(tmp_path, cars, clients):
    path = tmp_path / "bookings.json"
    path.write_text(json.dumps([{
        "id": 1,
        "car_id": 99,
        "client_id": 1,
        "start_date": "2026-10-10",
        "end_date": "2026-10-12",
        "is_cancelled": False,
    }]), encoding="utf-8")

    with pytest.raises(ValueError):
        load_bookings(str(path), cars, clients)


def test_load_broken_json_raises(tmp_path):
    path = tmp_path / "cars.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_cars(str(path))


def test_project_data_files_are_consistent():
    cars = load_cars("data/cars.json")
    clients = load_clients("data/clients.json")
    bookings = load_bookings("data/bookings.json", cars, clients)

    assert len(cars) == 6
    assert len(clients) == 5
    assert len(bookings) == 8
