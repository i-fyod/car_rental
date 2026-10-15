"""Вспомогательные функции: ввод данных, даты, идентификаторы."""
from datetime import date
from typing import Iterable, Optional, Protocol


class HasId(Protocol):
    id: int


def parse_date(value: str) -> date:
    """Преобразовать строку YYYY-MM-DD в дату (ValueError при ошибке)."""
    return date.fromisoformat(value)


def is_valid_date(value: str) -> bool:
    """Проверить, что строка является датой в формате YYYY-MM-DD."""
    try:
        parse_date(value)
    except ValueError:
        return False
    return True


def next_id(items: Iterable[HasId]) -> int:
    """Вернуть следующий свободный идентификатор для коллекции."""
    return max((item.id for item in items), default=0) + 1


def input_int(prompt: str, min_value: Optional[int] = None) -> int:
    """Запросить целое число, повторяя ввод до корректного значения."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Введите целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Число должно быть не меньше {min_value}.")
            continue
        return value


def input_date(prompt: str) -> str:
    """Запросить дату YYYY-MM-DD, повторяя ввод до корректного значения."""
    while True:
        raw = input(prompt).strip()
        if is_valid_date(raw):
            return raw
        print("Введите дату в формате ГГГГ-ММ-ДД, например 2026-10-20.")
