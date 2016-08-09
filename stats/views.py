import pygal

from scipy import stats

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from budget.models import Entry, Category
from budget.forms import EntryForm, CategoryForm

def get_savings_over_time(user):
    entries = Entry.objects.filter(user=user).order_by('date', 'date_created')
    savings = [0]
    for entry in entries:
        if entry.flow_type == Entry.EXPENSE:
            savings.append(int(savings[-1] - entry.value))
        else:
            savings.append(int(savings[-1] + entry.value))
    return savings

def get_line_of_best_fit(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return [(0, intercept), (len(x), intercept + slope * len(x))]

def get_savings_over_time_graph(user):
    savings = get_savings_over_time(user)
    chart = pygal.XY()
    x = range(len(savings))
    y = savings
    chart.add('Savings', list(zip(x, y)))
    chart.add('Linear', get_line_of_best_fit(range(len(savings)), savings))
    return chart.render()

@login_required
def stats_home(request):
    template = 'home.html'
    context = {
        'savings_over_time': get_savings_over_time_graph(request.user),
    }
    return render(request, template, context)
