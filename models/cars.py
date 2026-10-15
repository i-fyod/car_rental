"""Автомобили: класс Car и функции работы с коллекцией List[Car]."""
from typing import List, Optional

from utils import next_id


class Car:
    """Автомобиль, доступный для аренды."""

    def __init__(
        self,
        car_id: int,
        name: str,
        seats: int,
        car_type: str,
        price_per_day: int,
        description: str = "",
    ) -> None:
        """Создать объект автомобиля."""
        self.id = car_id
        self.name = name
        self.seats = seats
        self.car_type = car_type
        self.price_per_day = price_per_day
        self.description = description

    @classmethod
    def from_data(cls, data: dict) -> "Car":
        """Создать автомобиль из словаря, прочитанного из JSON."""
        return cls(
            car_id=data["id"],
            name=data["name"],
            seats=data["seats"],
            car_type=data["car_type"],
            price_per_day=data["price_per_day"],
            description=data.get("description", ""),
        )

    @staticmethod
    def validate_seats(seats: int) -> bool:
        """Проверить корректность числа мест."""
        return 1 <= seats <= 20

    def is_suitable_for(self, people_count: int) -> bool:
        """Проверить, вместит ли автомобиль указанное число людей."""
        return self.seats >= people_count

    def __str__(self) -> str:
        """Вернуть строковое представление автомобиля."""
        return (
            f"{self.name} ({self.car_type}), {self.seats} мест, "
            f"{self.price_per_day} руб./сутки"
        )


def find_car_by_id(cars: List[Car], car_id: int) -> Optional[Car]:
    """Найти автомобиль по идентификатору."""
    for car in cars:
        if car.id == car_id:
            return car
    return None


def add_car(
    cars: List[Car],
    name: str,
    seats: int,
    car_type: str,
    price_per_day: int,
    description: str = "",
) -> Car:
    """Создать автомобиль, добавить его в коллекцию и вернуть."""
    if not Car.validate_seats(seats):
        raise ValueError("Число мест должно быть от 1 до 20.")
    if price_per_day <= 0:
        raise ValueError("Цена за сутки должна быть положительной.")
    car = Car(next_id(cars), name, seats, car_type, price_per_day,
              description)
    cars.append(car)
    return car


def find_car(cars: List[Car], query: str) -> List[Car]:
    """Найти автомобили по части названия или типа кузова."""
    text = query.strip().lower()
    return [
        car for car in cars
        if text in car.name.lower() or text in car.car_type.lower()
    ]


def check_car_seats(cars: List[Car], car_id: int, min_seats: int) -> bool:
    """Проверить, что автомобиль существует и вмещает min_seats человек."""
    car = find_car_by_id(cars, car_id)
    return car is not None and car.is_suitable_for(min_seats)


def filter_cars_by_seats(cars: List[Car], min_seats: int) -> List[Car]:
    """Отобрать автомобили с числом мест не меньше min_seats."""
    return [car for car in cars if car.is_suitable_for(min_seats)]


def sort_cars(
    cars: List[Car],
    key: str = "price",
    reverse: bool = False,
) -> List[Car]:
    """Вернуть автомобили, отсортированные по price, seats или name."""
    keys = {
        "price": lambda car: car.price_per_day,
        "seats": lambda car: car.seats,
        "name": lambda car: car.name.lower(),
    }
    if key not in keys:
        raise ValueError(f"Неизвестный ключ сортировки: {key}")
    return sorted(cars, key=keys[key], reverse=reverse)


def show_cars(cars: List[Car]) -> None:
    """Вывести список автомобилей в консоль."""
    if not cars:
        print("Автомобили не найдены.")
        return
    for car in cars:
        print(f"{car.id}. {car}")
