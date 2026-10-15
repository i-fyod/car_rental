import pytest

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
