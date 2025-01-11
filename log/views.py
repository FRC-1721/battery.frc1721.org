from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry
from .forms import EntryForm

from battery.settings import BAD_KEY
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            entries = Entry.objects.all()
            form = EntryForm()
            return HttpResponseRedirect("/")
            #return render(request, 'index.html', {'entries': entries, 'form': form, 'message': 'USER NOT AUTHENTICATED. PLEASE LOG IN.'})

        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            entry = Entry(
                battery   = data['battery'],
                ready     = data['ready'],
                condition = data['condition'],
                charge    = data['charge'],
                rint      = data['rint'],
                memo      = data['memo'],
                user      = request.user.username
            )
            entry.save()

        return HttpResponseRedirect("/")


    entries = list(map(
        lambda e:
            e.update({'user': (User.objects.filter(username=e['user']).first() or User(first_name=e['user'])).first_name})
            or e.update({'condition': Entry.Condition(e['condition']).label or "N/A"})
            or e.update({'memo': e['memo'] or ''})
            or e.update({'date': e['date'].strftime("%d %b, %Y %H:%M:%S")})
            or e,
        map(lambda x: x.__dict__, Entry.objects.order_by('date').reverse())
    ))

    form = EntryForm()
    return render(request, 'index.html', {'entries': entries, 'form': form, 'bad_key': BAD_KEY})
