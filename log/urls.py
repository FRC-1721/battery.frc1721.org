from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.index,
        name="index",
    ),
    path(
        "battery/<str:battery_id>/",
        views.battery_detail,
        name="battery_detail",
    ),
    path(
        "meta/getcoverimage/<str:battery_id>/",
        views.get_cover_image,
        name="get_cover_image",
    ),
]
