from django.urls import path
from log.views import (
    IndexView,
    BatteryDetailView,
    GetCoverImageView,
    SubmitEntryView,
    BatteryLabelView,
)

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
    path(
        "submit/",
        SubmitEntryView.as_view(),
        name="submit_entry",
    ),
    path(
        "submit/<str:battery_id>/",  # Optional mode with pre-populated battery_id
        SubmitEntryView.as_view(),
        name="submit_entry_with_id",
    ),
    path(
        "label/<str:battery_id>/",
        BatteryLabelView.as_view(),
        name="battery_label",
    ),
]
