from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry
from .forms import EntryForm

from battery.settings import BAD_KEY
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    # Fetch unique battery names from the database
    unique_entries = Entry.objects.order_by(
        "battery", "-date"  # Order by battery, then most recent date
    ).distinct(
        "battery"  # Select one entry per unique battery
    )

    print(len(unique_entries))

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
            "available_batteries": unique_entries,  # Pass to the template
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
        {"battery_id": battery_id, "entries": entries},
    )
