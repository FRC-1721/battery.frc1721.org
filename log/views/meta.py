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


# Cover Image View
class GetCoverImageView(View):
    def get(self, request, battery_id):
        # Fetch the most recent entry for the battery
        entry = Entry.objects.filter(battery=battery_id).order_by("-date").first()
        if not entry:
            raise Http404("Battery not found")

        # Image dimensions
        width, height = 1200, 630

        # Create the image
        image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Fonts
        try:
            title_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 48)
            subtitle_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 36)
        except IOError:
            logging.warning("Using fallback fonts...")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Add content to the image
        draw.text((50, 50), f"Battery: {entry.battery}", font=title_font, fill="black")
        details = [
            f"Condition: {entry.condition}",
            f"Charge: {entry.charge}",
            f"User: {entry.user}",
        ]
        y_offset = 150
        for line in details:
            draw.text((50, y_offset), line, font=subtitle_font, fill="gray")
            y_offset += 50

        # Save the image to a buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Return the image as an HTTP response
        return HttpResponse(buffer, content_type="image/png")
