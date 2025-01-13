from django.http import Http404
from django.views.generic import ListView
from log.models import Entry


class BatteryDetailView(ListView):
    model = Entry
    template_name = "battery_detail.html"
    context_object_name = "entries"

    def get_queryset(self):
        # Filter entries by the battery ID provided in the URL

        battery_id = self.kwargs.get("battery_id")
        queryset = Entry.objects.filter(battery=battery_id).order_by("-date")
        if not queryset.exists():  # Check if the queryset is empty
            raise Http404(f"No entries found for battery '{battery_id}'")
        return queryset

    def get_context_data(self, **kwargs):
        # Add the battery_id to the context for use in the template
        context = super().get_context_data(**kwargs)
        context["battery_id"] = self.kwargs["battery_id"]
        return context
