from django.shortcuts import render

from models.bookings import find_booking_by_id
from storage import load_all


def bookings(request):
    """Список бронирований."""
    _, _, bookings_list = load_all()
    context = {
        "bookings": bookings_list,
    }
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    """Страница отдельного бронирования."""
    _, _, bookings_list = load_all()
    booking = find_booking_by_id(bookings_list, booking_id)

    context = {
        "booking": booking,
    }
    return render(
        request,
        "bookings/booking_detail.html",
        context,
        status=404 if booking is None else 200,
    )
