import pytest

from models import Client
from models.clients import (
    add_client,
    find_client,
    find_client_by_id,
)


def test_client_creation():
    client = Client(1, "Иван Петров", "ivan@example.com", "+7 900")

    assert client.id == 1
    assert client.name == "Иван Петров"
    assert client.email == "ivan@example.com"
    assert client.phone == "+7 900"


def test_client_str():
    client = Client(1, "Иван Петров", "ivan@example.com")

    assert str(client) == "Иван Петров <ivan@example.com>"


def test_client_from_data():
    client = Client.from_data({
        "id": 3,
        "name": "Анна Смирнова",
        "email": "anna@example.com",
    })

    assert client.id == 3
    assert client.phone == ""


def test_validate_email():
    assert Client.validate_email("a@b.ru")
    assert not Client.validate_email("a@b")
    assert not Client.validate_email("@b.ru")
    assert not Client.validate_email("abc")


def test_find_client_by_id(clients):
    assert find_client_by_id(clients, 2) is clients[1]
    assert find_client_by_id(clients, 99) is None


def test_add_client(clients):
    client = add_client(clients, "Олег Орлов", "oleg@example.com")

    assert client.id == 3
    assert clients[-1] is client


def test_add_client_rejects_bad_email(clients):
    with pytest.raises(ValueError):
        add_client(clients, "Олег Орлов", "oleg")
    assert len(clients) == 2


def test_find_client(clients):
    assert find_client(clients, "анна") == [clients[1]]
    assert find_client(clients, "ivan@") == [clients[0]]
    assert find_client(clients, "никого") == []
