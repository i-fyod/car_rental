from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.bookings import find_booking_by_id
from storage import load_all


def bookings(request):
    """Список бронирований."""
    _, _, bookings_list = load_all()
    items = ""
    for booking in bookings_list:
        status = "отменена" if booking.is_cancelled else "активна"
        badge = "bg-secondary" if booking.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/bookings/{booking.id}/">
                {escape(booking.car.name)}:
                {booking.start_date} – {booking.end_date}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Бронирования</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Бронирования", content))


def booking_detail(request, booking_id):
    """Страница отдельного бронирования."""
    _, _, bookings_list = load_all()
    booking = find_booking_by_id(bookings_list, booking_id)

    if booking is None:
        content = """
        <h1 class="text-danger">Бронирование не найдено</h1>
        <a href="/bookings/" class="btn btn-outline-secondary">
            ← к списку бронирований
        </a>
        """
        return HttpResponse(
            page("Бронирование не найдено", content),
            status=404,
        )

    status = "отменена" if booking.is_cancelled else "активна"
    badge = "bg-secondary" if booking.is_cancelled else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Бронирование №{booking.id}</h5>
            <p class="card-text">
                Автомобиль:
                <a href="/cars/{booking.car.id}/">
                    {escape(booking.car.name)}
                </a>
            </p>
            <p class="card-text">
                Клиент: {escape(booking.client.name)}
            </p>
            <p class="card-text">
                Период: {booking.start_date} – {booking.end_date}
                ({booking.days()} сут.)
            </p>
            <p class="card-text">
                Стоимость: {booking.total_price()} руб.
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/bookings/" class="btn btn-outline-secondary">
                ← к списку бронирований
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Бронирование №{booking.id}", content))
