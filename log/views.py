import os
import io

import logging

from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry
from .forms import EntryForm

from battery.settings import BAD_KEY
from django.contrib.auth.models import User

from PIL import Image, ImageDraw, ImageFont

# Create your views here.


def index(request):
    # Fetch unique battery names from the database
    unique_entries = Entry.objects.order_by(
        "battery", "-date"  # Order by battery, then most recent date
    ).distinct(
        "battery"  # Select one entry per unique battery
    )

    # When post...
    if request.method == "POST":
        # Cant be not authenticated!
        if not request.user.is_authenticated:
            entries = Entry.objects.all()
            form = EntryForm()
            return HttpResponseRedirect("/")
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            entry = Entry(
                battery=data["battery"],
                ready=data["ready"],
                condition=data["condition"],
                charge=data["charge"],
                rint=data["rint"],
                memo=data["memo"],
                user=request.user.username,
            )
            entry.save()
        return HttpResponseRedirect("/")

    entries = list(
        map(
            lambda e: e.update(
                {
                    "user": (
                        User.objects.filter(username=e["user"]).first()
                        or User(first_name=e["user"])
                    ).first_name
                }
            )
            or e.update({"condition": Entry.Condition(e["condition"]).label or "N/A"})
            or e.update({"memo": e["memo"] or ""})
            or e.update({"date": e["date"].strftime("%d %b, %Y %H:%M:%S")})
            or e,
            map(lambda x: x.__dict__, unique_entries),
        )
    )

    form = EntryForm()
    return render(
        request,
        "index.html",
        {
            "entries": entries,
            "form": form,
            "bad_key": BAD_KEY,
            "available_batteries": unique_entries,
        },
    )


def battery_detail(request, battery_id):
    # Fetch and filter entries by battery_id
    entries = Entry.objects.filter(battery=battery_id)

    # 404 for non-existent entries
    if not entries.exists():
        return render(
            request, "404.html", {"message": "Battery not found!"}, status=404
        )

    return render(
        request,
        "battery_detail.html",
        {
            "battery_id": battery_id,
            "entries": entries,
        },
    )


def get_cover_image(request, battery_id):
    # Fetch the entry data
    entry = Entry.objects.filter(battery=battery_id).order_by("-date").first()
    if not entry:
        return HttpResponse(status=404)  # Whoops lol, 404 cant help you

    # Image dimensions
    width, height = 1200, 630  # Opengraph/twitter size (discord likes it, dont ask)

    # Create an image with a background color
    image = Image.new("RGB", (width, height), (255, 255, 255))  # White background
    draw = ImageDraw.Draw(image)

    # Fonts
    try:
        title_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 48)
        subtitle_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 36)
    except IOError:
        # Fallback if font isn't available
        logging.warn("get_cover_image.py is using fallback fonts...")

        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Add a title to the image
    title = f"Battery: {entry.battery}"
    draw.text((50, 50), title, font=title_font, fill="black")

    # Add additional details
    details = [
        f"Condition: {entry.condition}",
        f"Charge: {entry.charge}",
        f"User: {entry.user}",
    ]
    y_offset = 150
    for line in details:
        draw.text((50, y_offset), line, font=subtitle_font, fill="gray")
        y_offset += 50

    # Save the image to a BytesIO buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the image as an HTTP response
    return HttpResponse(buffer, content_type="image/png")
