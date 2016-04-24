from django.shortcuts import render
from django.http import HttpResponse

from budget.models import Entry
from budget.forms import EntryForm

def index(request):
    template = 'index.html'

    context = {}

    return render(request, template, context)

def entry_list(request):
    template = 'entry_list.html'

    context = {
        'entries': Entry.objects.all(),
    }

    return render(request, template, context)

def entry_edit(request):
    template = 'entry_edit.html'


    return render(request, template, context)

def entry_create(request):
    template = 'entry_create.html'
    context = {}

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = EntryForm()

    context['form'] = form
    context['has_error'] = not form.errors == {}

    return render(request, template, context)
