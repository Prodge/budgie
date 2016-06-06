from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from budget.models import Entry
from budget.forms import EntryForm

@login_required
def home(request):
    template = 'index.html'
    context = {}
    return render(request, template, context)

@login_required
def entry_list(request):
    template = 'entry_list.html'
    context = {
        'entries': Entry.objects.filter(user = request.user),
    }
    return render(request, template, context)

@login_required
def entry_detail(request, entry_id):
    template = 'entry_detail.html'
    entry = Entry.objects.get(id = entry_id)
    context = {
        'entry': entry,
    }
    return render(request, template, context)

@login_required
def entry_edit(request, entry_id):
    template = 'entry_edit.html'
    entry = Entry.objects.get(id = entry_id)
    context = {
        'entry': entry,
    }

    if request.method == 'POST':
        form = EntryForm(request.POST, instance = entry)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = EntryForm(user = request.user, instance = entry)

    context['form'] = form
    return render(request, template, context)

@login_required
def entry_create(request):
    template = 'entry_edit.html'
    context = {}

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit = False)
            entry.user = request.user
            entry.save()
            context['success'] = True
    else:
        form = EntryForm(user = request.user)

    context['form'] = form
    context['has_error'] = not form.errors == {}

    return render(request, template, context)
