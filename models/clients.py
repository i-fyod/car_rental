"""Клиенты: класс Client и функции работы с коллекцией List[Client]."""
from typing import List, Optional

from utils import next_id


class Client:
    """Клиент сервиса аренды автомобилей."""

    def __init__(
        self,
        client_id: int,
        name: str,
        email: str,
        phone: str = "",
    ) -> None:
        """Создать объект клиента."""
        self.id = client_id
        self.name = name
        self.email = email
        self.phone = phone

    @classmethod
    def from_data(cls, data: dict) -> "Client":
        """Создать клиента из словаря, прочитанного из JSON."""
        return cls(
            client_id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data.get("phone", ""),
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Грубая проверка адреса электронной почты."""
        name, _, domain = email.partition("@")
        return bool(name) and "." in domain

    def __str__(self) -> str:
        """Вернуть строковое представление клиента."""
        return f"{self.name} <{self.email}>"


def find_client_by_id(
    clients: List[Client],
    client_id: int,
) -> Optional[Client]:
    """Найти клиента по идентификатору."""
    for client in clients:
        if client.id == client_id:
            return client
    return None


def add_client(
    clients: List[Client],
    name: str,
    email: str,
    phone: str = "",
) -> Client:
    """Создать клиента, добавить его в коллекцию и вернуть."""
    if not Client.validate_email(email):
        raise ValueError("Некорректный адрес электронной почты.")
    client = Client(next_id(clients), name, email, phone)
    clients.append(client)
    return client


def find_client(clients: List[Client], query: str) -> List[Client]:
    """Найти клиентов по части имени или адреса почты."""
    text = query.strip().lower()
    return [
        client for client in clients
        if text in client.name.lower() or text in client.email.lower()
    ]


def show_clients(clients: List[Client]) -> None:
    """Вывести список клиентов в консоль."""
    if not clients:
        print("Клиенты не найдены.")
        return
    for client in clients:
        print(f"{client.id}. {client}")
