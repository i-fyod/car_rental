# Сервис аренды автомобилей

Учебный индивидуальный проект: автомобили, клиенты и бронирования на период.

## Классы

| Класс | Назначение | Основные атрибуты |
|---|---|---|
| `Car` | автомобиль | `id`, `name`, `seats`, `car_type`, `price_per_day`, `description` |
| `Client` | клиент | `id`, `name`, `email`, `phone` |
| `Booking` | бронирование автомобиля клиентом | `id`, `car`, `start_date`, `end_date`, `client`, `is_cancelled` |

`Booking` хранит ссылки на объекты `Car` и `Client`, а в JSON сохраняются только их идентификаторы.
Активная бронь блокирует автомобиль на весь период, отменённая не блокирует.

## Структура

```
car_rental/
├── main.py            # консольное меню
├── storage.py         # загрузка и сохранение JSON
├── utils.py           # ввод данных, даты, идентификаторы
├── models/            # классы и функции предметной области
├── data/              # cars.json, clients.json, bookings.json
├── tests/             # pytest
├── requirements.txt
└── README.md
```

## Запуск

```bash
python3.11 -m venv venv
source venv/bin/activate        # fish: source venv/bin/activate.fish
pip install -r requirements.txt
python main.py
```

## Проверки

```bash
pytest -v
flake8 . --extend-exclude=venv
```
