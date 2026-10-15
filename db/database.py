"""Подключение к базе данных SQLite проекта."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "data" / "carrental.sqlite")
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    """Открыть соединение и включить проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    # По умолчанию SQLite не проверяет внешние ключи.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Создать таблицы из sql/schema.sql (повторный запуск безопасен)."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
