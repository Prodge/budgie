import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from budget.models import Entry, Category
from budget.forms import EntryForm, CategoryForm

def get_amount_spent(entries):
    return sum([float(entry.value) for entry in entries if entry.flow_type != Entry.INCOME])

def get_earliest_entry_date(entries):
    return min([entry.date for entry in entries])

def get_average_spent_over_period(entries, period):
    today = datetime.date.today()
    earliest_entry = get_earliest_entry_date(entries)
    days_since_first_entry = (today - earliest_entry).days
    segments = days_since_first_entry / period
    return get_amount_spent(entries) / segments

def filter_entries_to_period(entries, period):
    today = datetime.date.today()
    return entries.filter(date__gte = today - datetime.timedelta(days = period))

def get_amount_spent_over_period(entries, period):
    return get_amount_spent(filter_entries_to_period(entries, period))

def get_home_page_summary(entries):
    return {
        'week': get_amount_spent_over_period(entries, 7),
        'average_week': get_average_spent_over_period(entries, 7),
        'month': get_amount_spent_over_period(entries, 30),
        'average_month': get_average_spent_over_period(entries, 30),
    }

@login_required
def home(request):
    template = 'index.html'
    entries = Entry.objects.filter(user = request.user)
    context = {
        'spendings': get_home_page_summary(entries)
    }
    return render(request, template, context)

@login_required
def entry_list(request):
    template = 'entry_list.html'
    context = {}
    if request.POST:
        entry_ids = [int(entry_id) for entry_id, state in dict(request.POST).items() if state == ['on']]
        Entry.objects.filter(id__in = entry_ids).delete()
        context['success'] = True
    context['entries'] = Entry.objects.filter(user = request.user).order_by('-date', '-date_created')
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
    context = {}
    if request.POST:
        category_ids = [int(category_id) for category_id, state in dict(request.POST).items() if state == ['on']]
        Category.objects.filter(id__in = category_ids).delete()
        context['success'] = True
    context['categories'] = Category.objects.filter(user = request.user)
    return render(request, template, context)

def get_category_summary(category):
    entries = Entry.objects.filter(category = category)
    today = datetime.date.today()
    summary = {
        'forever': get_amount_spent(entries),
        'week': get_amount_spent_over_period(entries, 7),
        'month': get_amount_spent_over_period(entries, 30),
        'year': get_amount_spent_over_period(entries, 365),
    }
    summary['average_week_over_month'] = summary['month'] / (30 / 7)
    summary['average_week_over_year'] = summary['year'] / (365 / 7)
    summary['average_month_over_year'] = summary['year'] / 12
    return summary

@login_required
def category_detail(request, category_id):
    template = 'category_detail.html'
    category = Category.objects.get(id = category_id)
    context = {
        'category': category,
        'spendings': get_category_summary(category),
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
