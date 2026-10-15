"""Перенос данных из JSON-файлов в таблицы SQLite.

Запуск из корня проекта: python -m db.import_json
"""
import json
import sqlite3
from typing import Any, Dict, List

from db.database import create_schema, get_connection
from storage import BOOKINGS_PATH, CARS_PATH, CLIENTS_PATH

TABLES = ("cars", "clients", "bookings")


def load_json(filename: str) -> List[Dict[str, Any]]:
    """Прочитать список записей из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn: sqlite3.Connection) -> None:
    """Очистить таблицы, чтобы импорт можно было запускать повторно."""
    # Сначала bookings: она ссылается на cars и clients.
    # Имена таблиц берутся из константы, а не из пользовательского ввода.
    for table in reversed(TABLES):
        conn.execute(f"DELETE FROM {table}")


def import_cars(conn: sqlite3.Connection) -> None:
    """Перенести автомобили."""
    conn.executemany(
        """
        INSERT INTO cars (id, name, seats, car_type, price_per_day,
                          description)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                car["id"],
                car["name"],
                car["seats"],
                car["car_type"],
                car["price_per_day"],
                car.get("description", ""),
            )
            for car in load_json(CARS_PATH)
        ],
    )


def import_clients(conn: sqlite3.Connection) -> None:
    """Перенести клиентов."""
    conn.executemany(
        """
        INSERT INTO clients (id, name, email, phone)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                client["id"],
                client["name"],
                client["email"],
                client.get("phone", ""),
            )
            for client in load_json(CLIENTS_PATH)
        ],
    )


def import_bookings(conn: sqlite3.Connection) -> None:
    """Перенести бронирования (после автомобилей и клиентов)."""
    conn.executemany(
        """
        INSERT INTO bookings (id, car_id, client_id, start_date, end_date,
                              is_cancelled)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                booking["id"],
                booking["car_id"],
                booking["client_id"],
                booking["start_date"],
                booking["end_date"],
                int(booking["is_cancelled"]),
            )
            for booking in load_json(BOOKINGS_PATH)
        ],
    )


def import_all(conn: sqlite3.Connection) -> None:
    """Создать схему и заново перенести все данные."""
    create_schema(conn)
    clear_tables(conn)
    # Порядок важен: внешние ключи bookings требуют готовых cars и clients.
    import_cars(conn)
    import_clients(conn)
    import_bookings(conn)


def count_rows(conn: sqlite3.Connection) -> Dict[str, int]:
    """Число записей в каждой таблице для сверки с JSON."""
    return {
        table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in TABLES
    }


def main() -> None:
    """Импортировать данные в рабочую базу и показать число записей."""
    conn = get_connection()
    try:
        import_all(conn)
        conn.commit()
        for table, count in count_rows(conn).items():
            print(f"{table}: {count}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
