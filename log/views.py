from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry
from .forms import EntryForm

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
                battery = data['battery'],
                ready = data['ready'],
                condition = data['condition'],
                charge = data['charge'],
                rint = data['rint'],
                memo = data['memo'],
                user=request.user.username
            )
            entry.save()

        
        return HttpResponseRedirect("/")

    entries = Entry.objects.all()
    form = EntryForm()
    return render(request, 'index.html', {'entries': entries,"form": form})
