import sqlite3

import pytest

import db.database
from db.import_json import import_all
from models import Car, Client


@pytest.fixture
def cars():
    return [
        Car(1, "Toyota Camry", 5, "седан", 4500),
        Car(2, "Ford Transit", 9, "микроавтобус", 6500),
        Car(3, "Skoda Fabia", 5, "хэтчбек", 2600),
    ]


@pytest.fixture
def clients():
    return [
        Client(1, "Иван Петров", "ivan@example.com", "+7 900 111-22-33"),
        Client(2, "Анна Смирнова", "anna@example.com"),
    ]


@pytest.fixture(scope="session")
def built_db(tmp_path_factory):
    """Временная база SQLite с данными из JSON."""
    path = str(tmp_path_factory.mktemp("db") / "test.sqlite")
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    import_all(conn)
    conn.commit()
    conn.close()
    return path


@pytest.fixture(autouse=True)
def use_test_db(built_db, monkeypatch):
    """Веб-страницы в тестах работают с временной базой."""
    monkeypatch.setattr(db.database, "DB_PATH", built_db)
