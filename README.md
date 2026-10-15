# Сервис аренды автомобилей

Учебный индивидуальный проект: автомобили, клиенты и бронирования на период.
Есть консольная версия (данные в JSON) и веб-интерфейс на Django 5.2 (данные в SQLite).

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
├── bookings/          # страницы бронирований, статистика и их шаблоны
├── db/                # database.py (подключение), import_json.py (импорт из JSON)
├── sql/               # schema.sql (таблицы), queries.sql (запросы)
├── main.py            # консольное меню
├── storage.py         # загрузка и сохранение JSON
├── utils.py           # ввод данных, даты, идентификаторы
├── models/            # классы и функции предметной области
├── data/              # cars.json, clients.json, bookings.json, carrental.sqlite
├── tests/             # pytest
├── requirements.txt
└── README.md
```

## Страницы

| URL | Имя маршрута | View | Шаблон |
|---|---|---|---|
| `/` | `homepage:index` | `homepage.views.index` | `homepage/index.html` |
| `/cars/` | `cars:list` | `cars.views.cars` | `cars/car_list.html` |
| `/cars/<id>/` | `cars:detail` | `cars.views.car_detail` | `cars/car_detail.html` |
| `/cars/available/?date=ГГГГ-ММ-ДД` | `cars:available` | `cars.views.available_cars` | `cars/available.html` |
| `/bookings/` | `bookings:list` | `bookings.views.bookings` | `bookings/booking_list.html` |
| `/bookings/<id>/` | `bookings:detail` | `bookings.views.booking_detail` | `bookings/booking_detail.html` |
| `/bookings/statistics/` | `bookings:statistics` | `bookings.views.statistics` | `bookings/statistics.html` |

Несуществующий идентификатор возвращает страницу с кодом 404; обработчик `handler404` объявлен в
`carrental/urls.py`, страница лежит в `homepage/templates/homepage/404.html`.

## Шаблоны и статика

- `templates/base.html` — общий каркас: Bootstrap 5.3 (CDN), собственный CSS, шапка с логотипом, блоки `title` и `content`, подвал и скрипт.
- Дочерние шаблоны наследуют его через `{% extends %}` и переопределяют блоки.
- Включаемые фрагменты (`{% include %}`): навигация (`includes/navigation.html`), карточка автомобиля (`cars/includes/car_card.html`) и статус брони (`bookings/includes/booking_status.html`).
- Данные приходят во view-функциях и передаются в шаблоны через контекст; циклы с `{% empty %}`, условия по `is_cancelled`, ссылки через `{% url %}` с пространствами имён приложений.
- Фильтры: `length`, `default`, `capfirst`, `truncatewords`.
- Статика в `homepage/static/homepage/`: `css/style.css`, `js/main.js` (текущий год и подсветка пункта меню), `img/logo.svg`.

## База данных SQLite

Файл `data/carrental.sqlite`, таблицы создаёт `sql/schema.sql`. ORM Django не используется: view-функции работают через `sqlite3`.

| Таблица | Поля |
|---|---|
| `cars` | `id` (PK), `name`, `seats`, `car_type`, `price_per_day`, `description` |
| `clients` | `id` (PK), `name`, `email`, `phone` |
| `bookings` | `id` (PK), `car_id` (FK → `cars.id`), `client_id` (FK → `clients.id`), `start_date`, `end_date`, `is_cancelled` (0 — активна, 1 — отменена) |

- Даты хранятся строками `ГГГГ-ММ-ДД`, поэтому их можно сравнивать и сортировать средствами SQL; на `bookings` есть проверка `end_date >= start_date`.
- `db/database.py` — `get_connection()` включает `PRAGMA foreign_keys = ON`, `create_schema()` выполняет `sql/schema.sql` (повторный запуск безопасен: `CREATE TABLE IF NOT EXISTS`).
- `db/import_json.py` — перенос данных из JSON: сначала `cars` и `clients`, потом `bookings`; перед импортом таблицы очищаются, поэтому скрипт можно запускать повторно. После переноса выводит число записей для сверки с JSON.
- `sql/queries.sql` — 14 проверенных запросов: SELECT, WHERE, JOIN, подзапрос `NOT IN` с `BETWEEN`, COUNT, MIN/MAX/AVG, GROUP BY, SUM и HAVING.
- Значения в запросы передаются только параметрами `?`; строки результата читаются по именам через `sqlite3.Row`.

Что показывают страницы:

- `/cars/`, `/cars/<id>/` и `/bookings/`, `/bookings/<id>/` — списки и карточки из таблиц (в бронях JOIN трёх таблиц, срок и стоимость считает SQL);
- `/cars/available/` — автомобили, свободные на выбранную дату;
- `/bookings/statistics/` — активные брони по автомобилям, выручка по типам кузова и автомобили минимум с двумя бронями.

Консольное приложение по-прежнему работает с JSON. После изменений в JSON базу нужно перенести заново.

## Запуск

```bash
python3.11 -m venv venv
source venv/bin/activate        # fish: source venv/bin/activate.fish
pip install -r requirements.txt

python -m db.import_json        # (пере)создать базу из JSON-файлов
python main.py                  # консольное приложение
python manage.py runserver      # веб-интерфейс: http://127.0.0.1:8000/
```

## Проверки

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv
```
