from django.urls import path
from log.views import IndexView, BatteryDetailView, GetCoverImageView

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path(
        "battery/<str:battery_id>/",
        BatteryDetailView.as_view(),
        name="battery_detail",
    ),
    path(
        "meta/getcoverimage/<str:battery_id>/",
        GetCoverImageView.as_view(),
        name="get_cover_image",
    ),
]
