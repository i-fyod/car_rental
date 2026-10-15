-- ==========================================
-- Прокат автомобилей: проверенные SQL-запросы
-- Значения подставляются параметрами ? (в SQLite CLI: .param set или замена вручную)
-- Проверка: sqlite3 data/carrental.sqlite
-- ==========================================


-- 1. SELECT: список автомобилей
SELECT
    id,
    name,
    seats,
    car_type,
    price_per_day,
    description
FROM cars
ORDER BY name;


-- 2. SELECT: список клиентов
SELECT
    id,
    name,
    email,
    phone
FROM clients
ORDER BY name;


-- 3. WHERE: автомобили с числом мест не меньше N (параметр: 7)
SELECT
    id,
    name,
    seats,
    price_per_day
FROM cars
WHERE seats >= ?
ORDER BY price_per_day;


-- 4. WHERE: автомобили заданного типа кузова (параметр: 'кроссовер')
SELECT
    id,
    name,
    price_per_day
FROM cars
WHERE car_type = ?
ORDER BY price_per_day;


-- 5. WHERE: активные (не отменённые) бронирования
SELECT
    id,
    car_id,
    client_id,
    start_date,
    end_date
FROM bookings
WHERE is_cancelled = 0
ORDER BY start_date;


-- 6. JOIN: бронирования с названием автомобиля и именем клиента
SELECT
    bookings.id,
    bookings.start_date,
    bookings.end_date,
    bookings.is_cancelled,
    cars.name AS car_name,
    clients.name AS client_name
FROM bookings
JOIN cars
    ON bookings.car_id = cars.id
JOIN clients
    ON bookings.client_id = clients.id
ORDER BY bookings.start_date;


-- 7. JOIN + WHERE: активные бронирования клиента (параметр: id клиента)
SELECT
    bookings.id,
    cars.name AS car_name,
    bookings.start_date,
    bookings.end_date
FROM bookings
JOIN cars
    ON bookings.car_id = cars.id
WHERE bookings.client_id = ?
  AND bookings.is_cancelled = 0
ORDER BY bookings.start_date;


-- 8. Подзапрос: автомобили, свободные на выбранную дату (параметр: '2026-10-15')
SELECT
    cars.id,
    cars.name,
    cars.seats,
    cars.car_type,
    cars.price_per_day
FROM cars
WHERE cars.id NOT IN (
    SELECT bookings.car_id
    FROM bookings
    WHERE bookings.is_cancelled = 0
      AND ? BETWEEN bookings.start_date AND bookings.end_date
)
ORDER BY cars.price_per_day;


-- 9. COUNT: число активных бронирований
SELECT COUNT(*) AS active_bookings
FROM bookings
WHERE is_cancelled = 0;


-- 10. MIN, MAX, AVG: цены за сутки по всему парку
SELECT
    MIN(price_per_day) AS min_price,
    MAX(price_per_day) AS max_price,
    ROUND(AVG(price_per_day)) AS avg_price
FROM cars;


-- 11. GROUP BY: число активных бронирований по каждому автомобилю
SELECT
    cars.id,
    cars.name AS car_name,
    COUNT(bookings.id) AS bookings_count
FROM cars
LEFT JOIN bookings
    ON cars.id = bookings.car_id
    AND bookings.is_cancelled = 0
GROUP BY cars.id, cars.name
ORDER BY bookings_count DESC, cars.name;


-- 12. GROUP BY + SUM: выручка по типам кузова (дни считаются включительно)
SELECT
    cars.car_type,
    COUNT(bookings.id) AS bookings_count,
    SUM(
        cars.price_per_day
        * (CAST(julianday(bookings.end_date)
                - julianday(bookings.start_date) AS INTEGER) + 1)
    ) AS revenue
FROM bookings
JOIN cars
    ON bookings.car_id = cars.id
WHERE bookings.is_cancelled = 0
GROUP BY cars.car_type
ORDER BY revenue DESC;


-- 13. GROUP BY + HAVING: автомобили минимум с двумя активными бронями
SELECT
    cars.name AS car_name,
    COUNT(bookings.id) AS bookings_count
FROM cars
JOIN bookings
    ON cars.id = bookings.car_id
WHERE bookings.is_cancelled = 0
GROUP BY cars.id, cars.name
HAVING COUNT(bookings.id) >= 2
ORDER BY bookings_count DESC, cars.name;


-- 14. GROUP BY: число бронирований (всех) по клиентам
SELECT
    clients.name AS client_name,
    COUNT(bookings.id) AS bookings_count
FROM clients
LEFT JOIN bookings
    ON clients.id = bookings.client_id
GROUP BY clients.id, clients.name
ORDER BY bookings_count DESC, clients.name;
