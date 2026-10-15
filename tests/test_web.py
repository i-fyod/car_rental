import pytest


@pytest.mark.parametrize("url", [
    "/",
    "/cars/",
    "/cars/1/",
    "/bookings/",
    "/bookings/1/",
])
def test_pages_open(client, url):
    response = client.get(url)

    assert response.status_code == 200
    assert "bootstrap" in response.content.decode()


def test_car_list_shows_cars_from_json(client):
    html = client.get("/cars/").content.decode()

    assert "Toyota Camry" in html
    assert "Ford Transit" in html


def test_car_detail_shows_data(client):
    html = client.get("/cars/5/").content.decode()

    assert "Ford Transit" in html
    assert "9" in html
    assert "микроавтобус" in html


def test_booking_detail_shows_linked_objects(client):
    html = client.get("/bookings/1/").content.decode()

    assert "Toyota Camry" in html
    assert "Иван Петров" in html
    assert "7 сут." in html


def test_booking_status_badges(client):
    html = client.get("/bookings/").content.decode()

    assert "активна" in html
    assert "отменена" in html


def test_missing_car_returns_404(client):
    response = client.get("/cars/999/")

    assert response.status_code == 404
    assert "Автомобиль не найден" in response.content.decode()


def test_missing_booking_returns_404(client):
    response = client.get("/bookings/999/")

    assert response.status_code == 404
    assert "Бронирование не найдено" in response.content.decode()


def test_unknown_path_uses_custom_404(client, settings):
    settings.DEBUG = False

    response = client.get("/nonexistent/")

    assert response.status_code == 404
    assert "404 – страница не найдена" in response.content.decode()


def test_non_numeric_id_is_not_routed(client, settings):
    settings.DEBUG = False

    assert client.get("/cars/abc/").status_code == 404
