import os
import io
import logging

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from django.db import connection
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
            return Entry.objects.filter(battery__in=batteries).order_by("-date")
        else:
            # PostgreSQL or compatible database with DISTINCT ON support
            return Entry.objects.order_by("battery", "-date").distinct("battery")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bad_key"] = BAD_KEY
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
        return HttpResponseRedirect("/")
