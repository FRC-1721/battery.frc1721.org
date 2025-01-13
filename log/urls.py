from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("battery/<str:battery_id>/", views.battery_detail, name="battery_detail"),
]
