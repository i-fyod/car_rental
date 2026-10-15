from django.urls import path

from . import views

app_name = "cars"

urlpatterns = [
    path("", views.cars, name="list"),
    path("<int:car_id>/", views.car_detail, name="detail"),
]
