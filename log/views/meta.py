import os
import io
import logging
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from log.models import Entry
from PIL import Image, ImageDraw, ImageFont
from django.utils.timesince import timesince


class GetCoverImageView(View):
    def get(self, request, battery_id):
        # Fetch the most recent entry for the battery
        entry = Entry.objects.filter(battery=battery_id).order_by("-date").first()
        if not entry:
            raise Http404("Battery not found")

        # Get battery age (time since the first entry)
        first_entry = Entry.objects.filter(battery=battery_id).order_by("date").first()
        battery_age = timesince(first_entry.date) if first_entry else "N/A"

        # Fetch the last few log entries
        recent_logs = (
            Entry.objects.filter(battery=battery_id).order_by("-date")[:5]
            if first_entry
            else []
        )

        # Image dimensions
        width, height = 1200, 630

        # Create the image
        image = Image.new("RGB", (width, height), (255, 255, 255))  # White background
        draw = ImageDraw.Draw(image)

        # Fonts
        try:
            title_font = ImageFont.truetype("static/fonts/OpenSans-Bold.ttf", 88)
            subtitle_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 44)
            small_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 28)
        except IOError:
            logging.warning("Using fallback fonts...")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Draw maroon banner
        draw.rectangle([0, 0, width, 100], fill=(128, 0, 0))  # Maroon background
        draw.text((30, -10), f"{entry.battery}", font=title_font, fill="white")

        # Draw black strip below
        draw.rectangle([0, 100, width, 120], fill="black")

        # Add battery details
        draw.text((30, 140), "Details:", font=subtitle_font, fill="black")
        draw.text(
            (30, 200),
            f"Age in Database: {battery_age}",
            font=small_font,
            fill="gray",
        )

        # Add recent log entries
        y_offset = 250
        draw.text((30, y_offset), "Recent Logs:", font=subtitle_font, fill="black")
        y_offset += 50
        for log in recent_logs:
            log_text = f"{log.date.strftime('%Y-%m-%d %H:%M')} - {log.user}: {log.memo}"
            draw.text((30, y_offset), log_text, font=small_font, fill="gray")
            y_offset += 40

        # Save the image to a buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Return the image as an HTTP response
        return HttpResponse(buffer, content_type="image/png")
