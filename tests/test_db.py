import json
import re
import shutil
import sqlite3
from pathlib import Path

import pytest

import db.database
from db.database import create_schema, get_connection
from db.import_json import count_rows, import_all
from storage import BOOKINGS_PATH, CARS_PATH, CLIENTS_PATH

QUERIES_PATH = Path("sql/queries.sql")

# Параметры запросов, у которых в тексте есть заполнители ?.
QUERY_PARAMS = {3: [7], 4: ["кроссовер"], 7: [1], 8: ["2026-10-15"]}


def load_queries():
    """Разобрать sql/queries.sql на запросы по номерам в комментариях."""
    text = QUERIES_PATH.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=-- \d+\. )", text)[1:]
    return {
        int(re.match(r"-- (\d+)\.", block).group(1)):
        block.strip().rstrip(";")
        for block in blocks
    }


def json_len(path):
    return len(json.loads(Path(path).read_text(encoding="utf-8")))


def test_import_counts_match_json():
    with get_connection() as conn:
        counts = count_rows(conn)

    assert counts == {
        "cars": json_len(CARS_PATH),
        "clients": json_len(CLIENTS_PATH),
        "bookings": json_len(BOOKINGS_PATH),
    }


def test_schema_can_be_applied_twice():
    conn = get_connection()
    try:
        create_schema(conn)
        create_schema(conn)
        tables = {
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'")
        }
    finally:
        conn.close()

    assert {"cars", "clients", "bookings"} <= tables


def test_import_can_be_repeated(tmp_path):
    path = tmp_path / "repeat.sqlite"
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")

    import_all(conn)
    import_all(conn)

    assert count_rows(conn)["bookings"] == json_len(BOOKINGS_PATH)
    conn.close()


def test_foreign_keys_are_enforced():
    with get_connection() as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO bookings (car_id, client_id, start_date, "
                "end_date) VALUES (?, ?, ?, ?)",
                [999, 1, "2026-11-01", "2026-11-02"],
            )


def test_end_date_check_constraint():
    with get_connection() as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO bookings (car_id, client_id, start_date, "
                "end_date) VALUES (?, ?, ?, ?)",
                [1, 1, "2026-11-05", "2026-11-02"],
            )


def test_queries_file_has_required_kinds():
    queries = load_queries()
    joined = {n: q.upper() for n, q in queries.items()}

    def count(word):
        return sum(1 for q in joined.values() if word in q)

    assert len(queries) >= 10
    assert count("WHERE") >= 2
    assert count("JOIN") >= 2
    assert count("COUNT(") >= 2
    assert count("GROUP BY") >= 2
    assert count("HAVING") >= 1


@pytest.mark.parametrize("number, rows", [
    (1, 6), (2, 5), (3, 1), (4, 2), (5, 6), (6, 8), (7, 1), (8, 4),
    (9, 1), (10, 1), (11, 6), (12, 3), (13, 2), (14, 5),
])
def test_every_query_runs(number, rows):
    sql = load_queries()[number]

    with get_connection() as conn:
        result = conn.execute(sql, QUERY_PARAMS.get(number, [])).fetchall()

    assert len(result) == rows


def test_aggregate_query_values():
    queries = load_queries()

    with get_connection() as conn:
        active = conn.execute(queries[9]).fetchone()[0]
        prices = conn.execute(queries[10]).fetchone()

    assert active == 6
    assert tuple(prices) == (2600, 6500, 4600)


def test_available_cars_exclude_busy_and_cancelled():
    sql = load_queries()[8]

    with get_connection() as conn:
        names = {r[1] for r in conn.execute(sql, ["2026-10-15"])}

    assert "Toyota Camry" not in names
    assert "Hyundai Solaris" not in names
    # бронь Tiguan на эти даты отменена, поэтому машина свободна
    assert "Volkswagen Tiguan" in names


def test_cars_page_reads_from_database(client, tmp_path, monkeypatch):
    changed = tmp_path / "changed.sqlite"
    shutil.copy(db.database.DB_PATH, changed)
    conn = sqlite3.connect(changed)
    conn.execute("UPDATE cars SET name = 'Lada Vesta' WHERE id = 1")
    conn.commit()
    conn.close()
    monkeypatch.setattr(db.database, "DB_PATH", str(changed))

    html = client.get("/cars/").content.decode()

    assert "Lada Vesta" in html
    assert "Toyota Camry" not in html


def test_available_page_without_date_shows_prompt(client):
    html = client.get("/cars/available/").content.decode()

    assert "Выберите дату" in html
    assert 'type="date"' in html


def test_available_page_filters_by_date(client):
    html = client.get("/cars/available/?date=2026-10-15").content.decode()

    assert "Дата: 2026-10-15" in html
    assert "Skoda Fabia" in html
    assert "Toyota Camry" not in html
    assert "Hyundai Solaris" not in html


def test_available_page_keeps_selected_date(client):
    html = client.get("/cars/available/?date=2026-10-15").content.decode()

    assert 'value="2026-10-15"' in html


def test_available_page_lists_all_when_free(client):
    # на 2030 год броней нет, поэтому свободны все шесть машин
    html = client.get("/cars/available/?date=2030-01-01").content.decode()

    assert html.count("car-card") >= 6


def test_available_page_rejects_bad_date(client):
    response = client.get("/cars/available/?date=' OR 1=1 --")

    assert response.status_code == 200
    assert "Введите дату в формате" in response.content.decode()


def test_available_page_no_cars_message(client, tmp_path, monkeypatch):
    path = tmp_path / "busy.sqlite"
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    import_all(conn)
    conn.execute("DELETE FROM bookings")
    for car_id in range(1, 7):
        conn.execute(
            "INSERT INTO bookings (car_id, client_id, start_date, "
            "end_date) VALUES (?, 1, '2031-01-01', '2031-01-05')",
            [car_id],
        )
    conn.commit()
    conn.close()
    monkeypatch.setattr(db.database, "DB_PATH", str(path))

    html = client.get("/cars/available/?date=2031-01-03").content.decode()

    assert "свободных автомобилей нет" in html


def test_booking_pages_use_join_data(client):
    html = client.get("/bookings/").content.decode()

    assert "Toyota Camry" in html
    assert "Иван Петров" in html

    detail = client.get("/bookings/1/").content.decode()

    assert "7 сут." in detail
    assert "31500" in detail


def test_statistics_page(client):
    html = client.get("/bookings/statistics/").content.decode()

    assert "Статистика бронирований" in html
    assert "Выручка по типам кузова" in html
    assert "73500" in html
    assert "Toyota Camry" in html
    assert "Автомобили с двумя и более бронями" in html


def test_navigation_has_statistics_link(client):
    html = client.get("/").content.decode()

    assert 'href="/bookings/statistics/"' in html
