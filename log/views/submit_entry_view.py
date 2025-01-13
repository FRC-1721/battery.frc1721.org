import os
import logging

from django.views.generic import FormView
from log.models import Entry
from log.forms import EntryForm


class SubmitEntryView(FormView):
    form_class = EntryForm
    template_name = "submit_entry.html"
    success_url = "/"

    def get_initial(self):
        # Pre-fill the battery field if 'battery_id' is in the URL
        initial = super().get_initial()
        battery_id = self.kwargs.get("battery_id")
        if battery_id:
            initial["battery"] = battery_id

        return initial if not None else ""

    def get_context_data(self, **kwargs):
        # Pass available batteries to the context for the datalist
        context = super().get_context_data(**kwargs)
        context["available_batteries"] = Entry.objects.values_list(
            "battery", flat=True
        ).distinct()
        return context

    def form_valid(self, form):
        # Save the form with the current user
        data = form.cleaned_data
        Entry.objects.create(
            battery=data["battery"],
            ready=data["ready"],
            condition=data["condition"],
            charge=data["charge"],
            rint=data["rint"],
            memo=data["memo"],
            user=self.request.user.username,
        )
        return super().form_valid(form)
