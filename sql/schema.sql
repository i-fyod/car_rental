-- ==========================================
-- Прокат автомобилей: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    seats INTEGER NOT NULL,
    car_type TEXT NOT NULL,
    price_per_day INTEGER NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL DEFAULT ''
);

-- Даты хранятся строками YYYY-MM-DD, is_cancelled: 0 - активна, 1 - отменена
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    CHECK (end_date >= start_date),
    FOREIGN KEY (car_id) REFERENCES cars(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
