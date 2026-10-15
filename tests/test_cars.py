import pytest

from models import Car
from models.cars import (
    add_car,
    check_car_seats,
    filter_cars_by_seats,
    find_car,
    find_car_by_id,
    sort_cars,
)


def test_car_creation():
    car = Car(1, "Toyota Camry", 5, "седан", 4500, "Комфортный седан")

    assert car.id == 1
    assert car.name == "Toyota Camry"
    assert car.seats == 5
    assert car.car_type == "седан"
    assert car.price_per_day == 4500
    assert car.description == "Комфортный седан"


def test_car_str():
    car = Car(1, "Toyota Camry", 5, "седан", 4500)

    assert str(car) == "Toyota Camry (седан), 5 мест, 4500 руб./сутки"


def test_car_from_data():
    car = Car.from_data({
        "id": 7,
        "name": "Kia Rio",
        "seats": 5,
        "car_type": "седан",
        "price_per_day": 3100,
    })

    assert car.id == 7
    assert car.description == ""


def test_car_is_suitable_for():
    car = Car(1, "Toyota Camry", 5, "седан", 4500)

    assert car.is_suitable_for(5)
    assert not car.is_suitable_for(6)


def test_validate_seats():
    assert Car.validate_seats(5)
    assert not Car.validate_seats(0)
    assert not Car.validate_seats(21)


def test_find_car_by_id(cars):
    assert find_car_by_id(cars, 2) is cars[1]
    assert find_car_by_id(cars, 99) is None


def test_add_car(cars):
    car = add_car(cars, "Kia Rio", 5, "седан", 3100)

    assert car.id == 4
    assert cars[-1] is car
    assert len(cars) == 4


def test_add_car_rejects_bad_values(cars):
    with pytest.raises(ValueError):
        add_car(cars, "Bad", 0, "седан", 1000)
    with pytest.raises(ValueError):
        add_car(cars, "Bad", 5, "седан", 0)
    assert len(cars) == 3


def test_find_car(cars):
    assert find_car(cars, "toyota") == [cars[0]]
    assert find_car(cars, "ХЭТЧБЕК") == [cars[2]]
    assert find_car(cars, "нет такой") == []


def test_check_car_seats(cars):
    assert check_car_seats(cars, 2, 8)
    assert not check_car_seats(cars, 1, 8)
    assert not check_car_seats(cars, 99, 1)


def test_filter_cars_by_seats(cars):
    assert filter_cars_by_seats(cars, 6) == [cars[1]]
    assert len(filter_cars_by_seats(cars, 1)) == 3


def test_sort_cars(cars):
    assert sort_cars(cars, "price") == [cars[2], cars[0], cars[1]]
    assert sort_cars(cars, "seats", reverse=True)[0] is cars[1]
    assert sort_cars(cars, "name")[0] is cars[1]
    # исходная коллекция не меняется
    assert cars[0].name == "Toyota Camry"


def test_sort_cars_unknown_key(cars):
    with pytest.raises(ValueError):
        sort_cars(cars, "color")
