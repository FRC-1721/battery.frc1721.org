import os
import io
import logging

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View
from django.db import connection
from django.db.models import F, Value, IntegerField, CharField
from django.db.models.functions import Cast, Substr
from django.views.generic import TemplateView, ListView, DetailView, FormView
from log.models import Entry
from log.forms import EntryForm

from battery.settings import BAD_KEY
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.models import User


# Index View
class IndexView(ListView, FormView):
    model = Entry
    template_name = "index.html"
    context_object_name = "entries"
    form_class = EntryForm

    def get_queryset(self):
        if connection.vendor == "sqlite":
            # Workaround for SQLite (get latest for each battery manually)
            logging.warning("Skipping using psql DISTINCT because detected sqlite")

            batteries = Entry.objects.values_list("battery", flat=True).distinct()
            return (
                Entry.objects.filter(battery__in=batteries)
                .order_by("battery")
                .reverse()
            )
        else:
            # PostgreSQL (use DISTINCT ON with custom sorting)
            return (
                Entry.objects.annotate(
                    battery_number=Cast(Substr("battery", 1, 2), IntegerField()),
                    battery_letter=Substr("battery", 3, 1),
                )
                .order_by("battery", "-battery_number", "battery_letter")
                .distinct("battery")
                .reverse()
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Map the human-readable condition to each entry
        entries_with_labels = []
        for entry in context["entries"]:
            entry_dict = {
                "battery": entry.battery,
                "ready": entry.ready,
                "condition": entry.get_condition_display(),  # Get the human-readable label
                "charge": entry.charge,
                "rint": entry.rint,
                "memo": entry.memo,
                "user": entry.user,
                "date": entry.date.strftime("%d %b, %Y %H:%M:%S"),
            }
            entries_with_labels.append(entry_dict)
        context["entries"] = entries_with_labels

        return context

    def post(self, request, *args, **kwargs):
        # Handle form submission
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")

        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            Entry.objects.create(
                battery=data["battery"],
                ready=data["ready"],
                condition=data["condition"],
                charge=data["charge"],
                rint=data["rint"],
                memo=data["memo"],
                user=request.user.username,
            )
            return HttpResponseRedirect("/")  # Redirect only if form is valid
        else:
            logging.error("Form invalid: %s", form.errors)

        # Re-render the page with the form and errors
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "entries": self.get_queryset(),  # Pass entries to avoid breaking the template
                "bad_key": False,  # Or whatever other context your template uses
            },
        )
