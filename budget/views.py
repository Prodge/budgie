import datetime
import json

from collections import OrderedDict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from budget.models import Entry, Category
from budget.forms import EntryForm, CategoryForm

def get_total_value(entries):
    return sum([float(entry.value) for entry in entries])

def get_earliest_entry_date(entries):
    return min([entry.date for entry in entries])

def get_average_spent_over_period(entries, period):
    today = datetime.date.today()
    earliest_entry = get_earliest_entry_date(entries)
    days_since_first_entry = (today - earliest_entry).days
    segments = days_since_first_entry / period
    return get_total_value(entries) / segments

def filter_entries_to_period(entries, period):
    today = datetime.date.today()
    return entries.filter(date__gte = today - datetime.timedelta(days = period))

def get_value_over_period(entries, period):
    return get_total_value(filter_entries_to_period(entries, period))

def get_spending_summary(entries):
    entries = entries.filter(flow_type = Entry.EXPENSE)
    return {
        'week': get_value_over_period(entries, 7),
        'average_week': get_average_spent_over_period(entries, 7),
        'month': get_value_over_period(entries, 30),
        'average_month': get_average_spent_over_period(entries, 30),
    }

def get_income_summary(entries):
    entries = entries.filter(flow_type = Entry.INCOME)
    return {
        'year': get_value_over_period(entries, 360),
        'month': get_value_over_period(entries, 30),
        'week': get_value_over_period(entries, 7),
        'years_monthly_budget': get_value_over_period(entries, 365) / 12,
        'months_weekly_budget': get_value_over_period(entries, 30) / (30/7),
    }

def get_user_entries(user):
    return Entry.objects.filter(user=user)

def get_entry_occurances(entries):
    return {entry.label: entries.filter(label=entry.label).count() for entry in entries}

def get_sorted_entry_occurances(entries):
    return sorted(get_entry_occurances(entries).items(), key=lambda x: x[1], reverse=True)

def get_most_frequent_entries(entries, num):
    '''
    Returns a list of the most recent entry for each of the most common entry labels
    '''
    return [entries.filter(label = entry[0]).latest('id') for entry in get_sorted_entry_occurances(entries)[:num]]

def get_budget_status(spending_summary, income_summary):
    '''
    Green: you're under your budget and under your average.
    Blue: You're under your budget but not your average.
    Orange: your within 25% of your budget.
    Red: you're over 25% of your budget
    '''
    status = {
        'week': {'colour': '#b00', 'description': 'Over'},
        'month': {'colour': '#b00', 'description': 'Over'},
    }

    for period in status.keys():
        spent = spending_summary[period]
        budget_key = 'years_monthly_budget' if period == 'month' else 'months_weekly_budget'
        budget = income_summary[budget_key]
        average = spending_summary['average_{}'.format(period)]
        if spent < budget:
            if spent < average:
                status[period] = {'colour': '#0b0', 'description': 'Good'}
            else:
                status[period] = {'colour': '#00b', 'description': 'Ok'}
        if spent > budget * 0.75 and spent < budget * 1.25:
            status[period] = {'colour': '#E59400', 'description': 'Close'}
    return status

def get_entry_json_data(entry):
    return json.dumps({
        'label': entry.label,
        'value': float(entry.value),
        'flow_type': entry.flow_type,
        'category': entry.category.id,
        'essential': entry.essential,
        'description': entry.description,
    })

@login_required
def home(request):
    template = 'index.html'
    entries = Entry.objects.filter(user = request.user)
    spending_summary = get_spending_summary(entries)
    income_summary = get_income_summary(entries)
    context = {
        'spendings': spending_summary,
        'income': income_summary,
        'budget_status': get_budget_status(spending_summary, income_summary),
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
        context['frequent_entries'] = [(entry, get_entry_json_data(entry)) for entry in
                get_most_frequent_entries(
                    filter_entries_to_period(
                        get_user_entries(request.user), 60), 10)] # most frequent 10 in past 60 days # TODO make this a setting
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
    context['categories'] = Category.objects.filter(user = request.user).order_by('name')
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
