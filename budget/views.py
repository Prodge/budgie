from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from budget.models import Entry, Category
from budget.forms import EntryForm, CategoryForm

@login_required
def home(request):
    template = 'index.html'
    context = {}
    return render(request, template, context)

@login_required
def entry_list(request):
    template = 'entry_list.html'
    context = {}
    if request.POST:
        entry_ids = [int(entry_id) for entry_id, state in dict(request.POST).items() if state == ['on']]
        Entry.objects.filter(id__in = entry_ids).delete()
        context['success'] = True
    context['entries'] = Entry.objects.filter(user = request.user).order_by('-date')
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
        form = EntryForm(request.POST, instance = entry, user = request.user)
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
        form = EntryForm(request.POST, user = request.user)
        if form.is_valid():
            entry = form.save(commit = False)
            entry.user = request.user
            entry.save()
            return redirect('entry_detail', entry_id = entry.id)
    else:
        form = EntryForm(user = request.user)

    context['form'] = form
    context['has_error'] = not form.errors == {}

    return render(request, template, context)

@login_required
def category_list(request):
    template = 'category_list.html'
    context = {
        'categories': Category.objects.filter(user = request.user),
    }
    return render(request, template, context)

@login_required
def category_detail(request, category_id):
    template = 'category_detail.html'
    category = Category.objects.get(id = category_id)
    context = {
        'category': category
    }
    return render(request, template, context)

@login_required
def category_edit(request, category_id):
    template = 'category_edit.html'
    category = Category.objects.get(id = category_id)
    context = {
        'category': category
    }

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = category, user = request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = CategoryForm(instance = category, user = request.user)

    context['form'] = form
    return render(request, template, context)

@login_required
def category_create(request):
    template = 'category_edit.html'
    context = {}

    if request.method == 'POST':
        form = CategoryForm(request.POST, user = request.user)
        if form.is_valid():
            category = form.save(commit = False)
            category.user = request.user
            category.save()
            return redirect('category_detail', category_id = category.id)
    else:
        form = CategoryForm(user = request.user)

    context['form'] = form
    context['has_error'] = not form.errors == {}

    return render(request, template, context)
