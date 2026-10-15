# Сервис аренды автомобилей

Учебный индивидуальный проект: автомобили, клиенты и бронирования на период.
Есть консольная версия и веб-интерфейс на Django 5.2.

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
├── manage.py
├── carrental/         # Django-проект: настройки, корневые маршруты
├── homepage/          # главная страница, общий каркас страниц, страница 404
├── cars/              # страницы автомобилей
├── bookings/          # страницы бронирований
├── main.py            # консольное меню
├── storage.py         # загрузка и сохранение JSON
├── utils.py           # ввод данных, даты, идентификаторы
├── models/            # классы и функции предметной области
├── data/              # cars.json, clients.json, bookings.json
├── tests/             # pytest
├── requirements.txt
└── README.md
```

Django-приложения не используют ORM и базу данных: веб-слой загружает данные из JSON
функциями `storage.py` и вызывает функции из `models/`.

## Страницы

| URL | View | Назначение |
|---|---|---|
| `/` | `homepage.views.index` | главная страница и навигация |
| `/cars/` | `cars.views.cars` | список автомобилей |
| `/cars/<id>/` | `cars.views.car_detail` | карточка автомобиля, доступность на сегодня |
| `/bookings/` | `bookings.views.bookings` | список бронирований со статусами |
| `/bookings/<id>/` | `bookings.views.booking_detail` | бронирование: автомобиль, клиент, период, стоимость |

Несуществующий идентификатор возвращает страницу с кодом 404; обработчик `handler404` объявлен в
`carrental/urls.py`. HTML собирает функция `page()` из `homepage/views.py`, оформление через Bootstrap 5.3 (CDN).

## Запуск

```bash
python3.11 -m venv venv
source venv/bin/activate        # fish: source venv/bin/activate.fish
pip install -r requirements.txt

python main.py                  # консольное приложение
python manage.py runserver      # веб-интерфейс: http://127.0.0.1:8000/
```

## Проверки

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv
```
