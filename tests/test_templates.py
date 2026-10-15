import pytest
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.urls import reverse

import homepage.views


@pytest.mark.parametrize("name, args, path", [
    ("homepage:index", [], "/"),
    ("cars:list", [], "/cars/"),
    ("cars:detail", [3], "/cars/3/"),
    ("bookings:list", [], "/bookings/"),
    ("bookings:detail", [2], "/bookings/2/"),
])
def test_named_routes(name, args, path):
    assert reverse(name, args=args) == path


def test_pages_extend_base_template(client):
    for url in ["/", "/cars/", "/cars/1/", "/bookings/", "/bookings/1/"]:
        html = client.get(url).content.decode()

        assert 'class="nav site-nav"' in html
        assert "current-year" in html
        assert "homepage/css/style.css" in html
        assert "homepage/js/main.js" in html
        assert "homepage/img/logo.svg" in html


def test_navigation_links_are_built_from_routes(client):
    html = client.get("/").content.decode()

    assert 'href="/cars/"' in html
    assert 'href="/bookings/"' in html


def test_car_cards_link_to_detail_pages(client):
    html = client.get("/cars/").content.decode()

    assert 'href="/cars/1/"' in html
    assert "Всего автомобилей: 6" in html


def test_empty_car_list_shows_message():
    html = render_to_string("cars/car_list.html", {"cars": []})

    assert "Автомобили не найдены." in html
    assert "Всего автомобилей: 0" in html


def test_empty_booking_list_shows_message():
    html = render_to_string("bookings/booking_list.html", {"bookings": []})

    assert "Бронирований пока нет." in html


def test_cancelled_and_active_statuses_use_include(client):
    html = client.get("/bookings/").content.decode()

    assert "booking-status-active" in html
    assert "booking-status-cancelled" in html


def test_car_detail_not_found_template(client):
    response = client.get("/cars/999/")

    assert response.status_code == 404
    assert "Автомобиль не найден" in response.content.decode()
    assert 'href="/cars/"' in response.content.decode()


def test_static_files_are_found():
    for name in [
        "homepage/css/style.css",
        "homepage/js/main.js",
        "homepage/img/logo.svg",
    ]:
        assert finders.find(name) is not None


def test_html_is_escaped_in_templates():
    html = render_to_string(
        "cars/includes/car_card.html",
        {"car": type("C", (), {
            "id": 1, "name": "<b>X</b>", "car_type": "седан", "seats": 5,
            "price_per_day": 1, "description": "",
        })()},
    )

    assert "&lt;b&gt;X&lt;/b&gt;" in html


def test_page_helper_is_removed():
    assert not hasattr(homepage.views, "page")
