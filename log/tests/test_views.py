from django.test import TestCase
from django.urls import reverse
from log.models import Entry


class IndexViewTest(TestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class BatteryDetailViewTest(TestCase):
    def setUp(self):
        Entry.objects.create(battery="AA0", condition=Entry.Condition.GOOD)

    def test_battery_detail_view_status_code(self):
        response = self.client.get(reverse("battery_detail", args=["AA0"]))
        self.assertEqual(response.status_code, 200)

    def test_battery_detail_view_404(self):
        response = self.client.get(reverse("battery_detail", args=["NONEXISTENT"]))
        self.assertEqual(response.status_code, 404)
