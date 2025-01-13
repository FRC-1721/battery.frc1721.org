import os
import io
import logging

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
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
        # Fetch unique entries, ordered by battery and most recent date
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
