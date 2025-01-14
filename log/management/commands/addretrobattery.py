import random

from django.core.management.base import BaseCommand
from django.db import connection

from log.models import Entry

from datetime import datetime


class Command(BaseCommand):
    help = "Joe Wrote This. Adds a dummy battery entry for recordkeeping purposes"

    def handle(self, *args, **kwargs):
        # Prompt the user for inputs
        battery_id = input("Enter the battery ID (e.g., 22A): ").strip()
        year = input("Enter the year (e.g., 2022): ").strip()
        month = input("Enter the month (1-12): ").strip()

        try:
            # Convert year and month to integers
            year = int(year)
            month = int(month)

            # Validate the inputs
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12.")
            if year < 1900 or year > datetime.now().year:
                raise ValueError("Year must be a valid past or present year.")

            # Generate a random day in the given month
            day = random.randint(1, 28)  # (Safe for all months)
            date = datetime(year, month, day)

            # Insert the record directly using raw SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO log_entry (battery, ready, condition, charge, rint, memo, "user", date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        battery_id,
                        False,  # ready
                        1,  # condition (Good)
                        0.0,  # charge
                        0.0,  # rint
                        "System added entry for recordkeeping.",
                        "system",
                        date,
                    ],
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully added entry for battery '{battery_id}' dated {date.strftime('%Y-%m-%d')}."
                )
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
