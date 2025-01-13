from django.http import HttpResponse, Http404
from django.views import View
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import qrcode
from datetime import datetime
from log.models import Entry


class BatteryLabelView(View):
    def get(self, request, battery_id):
        # Check if the battery exists in the database
        if not Entry.objects.filter(battery=battery_id).exists():
            raise Http404("Battery not found")

        # Constants
        width, height = 1200, 500
        background_color = (255, 255, 255)  # White background
        text_color = (0, 0, 0)  # Black text
        maroon_color = (128, 0, 0)  # Maroon accent
        qr_size = 300  # QR code size

        # METADATA (Very important and epic)
        dpi = 1200  # Print resolution in DPI
        inches_width, inches_height = (
            width / dpi,
            height / dpi,
        )

        # Get the server version
        git_commit = os.getenv("GIT_COMMIT", "unknown")

        # Create the image
        image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(image)

        # Load fonts
        try:
            title_font = ImageFont.truetype("static/fonts/OpenSans-Bold.ttf", 140)
            subtitle_font = ImageFont.truetype("static/fonts/OpenSans-Regular.ttf", 46)
        except IOError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Add a maroon banner at the top
        draw.rectangle([0, 0, width, 160], fill=maroon_color)
        draw.text((30, -10), f"{battery_id}", font=title_font, fill="white")

        # Add details: date and server version
        date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text(
            (30, 160),
            f"Generated: {date_generated}",
            font=subtitle_font,
            fill=text_color,
        )
        draw.text(
            (30, 220),
            f"Server: {git_commit}",
            font=subtitle_font,
            fill=text_color,
        )

        # Add logo
        try:
            logo = Image.open("static/logos/tidalforceinvert.png").convert("RGBA")
            logo.thumbnail((145, 145))  # Resize to fit
            image.paste(logo, (width - 155, 10), logo)
        except FileNotFoundError:
            draw.text(
                (width - 300, 20),
                "Team Logo Missing",
                font=subtitle_font,
                fill=(255, 0, 0),
            )

        # Generate QR Code for submission URL
        url = f"{request.scheme}://{request.get_host()}/submit/{battery_id}/"
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_image = qr_image.resize((qr_size, qr_size), Image.LANCZOS)

        # Paste the QR Code on the right
        qr_x = width - qr_size - 20
        qr_y = height - qr_size - 20
        image.paste(qr_image, (qr_x, qr_y))

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        image.save(buffer, format="PNG", dpi=(dpi, dpi))
        buffer.seek(0)

        # Return the image as an HTTP response
        return HttpResponse(buffer, content_type="image/png")
