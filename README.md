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
├── templates/         # base.html и общие фрагменты (includes/navigation.html)
├── homepage/          # главная, страница 404, общая статика (css, js, img)
├── cars/              # страницы автомобилей и их шаблоны
├── bookings/          # страницы бронирований и их шаблоны
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

| URL | Имя маршрута | View | Шаблон |
|---|---|---|---|
| `/` | `homepage:index` | `homepage.views.index` | `homepage/index.html` |
| `/cars/` | `cars:list` | `cars.views.cars` | `cars/car_list.html` |
| `/cars/<id>/` | `cars:detail` | `cars.views.car_detail` | `cars/car_detail.html` |
| `/bookings/` | `bookings:list` | `bookings.views.bookings` | `bookings/booking_list.html` |
| `/bookings/<id>/` | `bookings:detail` | `bookings.views.booking_detail` | `bookings/booking_detail.html` |

Несуществующий идентификатор возвращает страницу с кодом 404; обработчик `handler404` объявлен в
`carrental/urls.py`, страница лежит в `homepage/templates/homepage/404.html`.

## Шаблоны и статика

- `templates/base.html` — общий каркас: Bootstrap 5.3 (CDN), собственный CSS, шапка с логотипом, блоки `title` и `content`, подвал и скрипт.
- Дочерние шаблоны наследуют его через `{% extends %}` и переопределяют блоки.
- Включаемые фрагменты (`{% include %}`): навигация (`includes/navigation.html`), карточка автомобиля (`cars/includes/car_card.html`) и статус брони (`bookings/includes/booking_status.html`).
- Данные приходят во view-функциях и передаются в шаблоны через контекст; циклы с `{% empty %}`, условия по `is_cancelled`, ссылки через `{% url %}` с пространствами имён приложений.
- Фильтры: `length`, `default`, `capfirst`, `truncatewords`.
- Статика в `homepage/static/homepage/`: `css/style.css`, `js/main.js` (текущий год и подсветка пункта меню), `img/logo.svg`.

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
