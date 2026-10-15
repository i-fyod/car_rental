"""Консольное приложение сервиса аренды автомобилей."""
from typing import List

from models import Booking, Car, Client
from models.bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    show_bookings,
)
from models.cars import (
    add_car,
    filter_cars_by_seats,
    find_car,
    find_car_by_id,
    show_cars,
    sort_cars,
)
from models.clients import (
    add_client,
    find_client,
    find_client_by_id,
    show_clients,
)
from storage import (
    BOOKINGS_PATH,
    load_bookings,
    load_cars,
    load_clients,
    save_bookings,
    save_cars,
    save_clients,
)
from utils import input_date, input_int

MENU = """
=== Аренда автомобилей ===
1. Показать автомобили
2. Найти автомобиль
3. Подобрать по числу мест
4. Отсортировать автомобили
5. Добавить автомобиль
6. Показать клиентов
7. Найти клиента
8. Добавить клиента
9. Показать бронирования
10. Создать бронирование
11. Отменить бронирование
12. Проверить доступность автомобиля
0. Сохранить и выйти
"""


def add_new_car(cars: List[Car]) -> None:
    """Запросить данные и добавить автомобиль."""
    name = input("Название: ").strip()
    seats = input_int("Число мест: ", 1)
    car_type = input("Тип кузова: ").strip()
    price = input_int("Цена за сутки: ", 1)
    try:
        car = add_car(cars, name, seats, car_type, price)
    except ValueError as error:
        print(error)
        return
    print(f"Добавлен автомобиль: {car}")


def add_new_client(clients: List[Client]) -> None:
    """Запросить данные и добавить клиента."""
    name = input("Имя: ").strip()
    email = input("Email: ").strip()
    phone = input("Телефон: ").strip()
    try:
        client = add_client(clients, name, email, phone)
    except ValueError as error:
        print(error)
        return
    print(f"Добавлен клиент: {client}")


def create_new_booking(
    bookings: List[Booking],
    cars: List[Car],
    clients: List[Client],
) -> None:
    """Запросить данные и создать бронирование через create_booking."""
    car = find_car_by_id(cars, input_int("ID автомобиля: "))
    if car is None:
        print("Автомобиль не найден.")
        return
    client = find_client_by_id(clients, input_int("ID клиента: "))
    if client is None:
        print("Клиент не найден.")
        return
    start = input_date("Начало аренды (ГГГГ-ММ-ДД): ")
    end = input_date("Конец аренды (ГГГГ-ММ-ДД): ")
    try:
        booking = create_booking(bookings, car, start, end, client)
    except ValueError as error:
        print(error)
        return
    if booking is None:
        print("Автомобиль занят в этот период.")
        return
    print(f"Создано: {booking}, итого {booking.total_price()} руб.")


def check_availability(bookings: List[Booking], cars: List[Car]) -> None:
    """Показать, свободен ли автомобиль в выбранный день."""
    car = find_car_by_id(cars, input_int("ID автомобиля: "))
    if car is None:
        print("Автомобиль не найден.")
        return
    day = input_date("Дата (ГГГГ-ММ-ДД): ")
    print(get_booking_status(bookings, car, day))


def sort_menu(cars: List[Car]) -> None:
    """Вывести автомобили в выбранном порядке."""
    print("Сортировка: 1 - по цене, 2 - по числу мест, 3 - по названию")
    keys = {1: "price", 2: "seats", 3: "name"}
    choice = input_int("Выбор: ")
    if choice not in keys:
        print("Неизвестный вариант.")
        return
    show_cars(sort_cars(cars, keys[choice]))


def main() -> None:
    """Загрузить данные, запустить меню и сохранить изменения."""
    try:
        cars = load_cars()
        clients = load_clients()
        bookings = load_bookings(BOOKINGS_PATH, cars, clients)
    except ValueError as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    actions = {
        1: lambda: show_cars(cars),
        2: lambda: show_cars(find_car(cars, input("Запрос: "))),
        3: lambda: show_cars(
            filter_cars_by_seats(cars, input_int("Мест не меньше: ", 1))
        ),
        4: lambda: sort_menu(cars),
        5: lambda: add_new_car(cars),
        6: lambda: show_clients(clients),
        7: lambda: show_clients(find_client(clients, input("Запрос: "))),
        8: lambda: add_new_client(clients),
        9: lambda: show_bookings(bookings),
        10: lambda: create_new_booking(bookings, cars, clients),
        11: lambda: print(
            "Бронь отменена."
            if cancel_booking(bookings, input_int("ID брони: "))
            else "Бронь не найдена."
        ),
        12: lambda: check_availability(bookings, cars),
    }

    while True:
        print(MENU)
        choice = input_int("Выбор: ")
        if choice == 0:
            break
        action = actions.get(choice)
        if action is None:
            print("Неизвестный пункт меню.")
            continue
        action()

    save_cars(cars)
    save_clients(clients)
    save_bookings(bookings)
    print("Данные сохранены.")


if __name__ == "__main__":
    main()
