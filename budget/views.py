from django.shortcuts import render
from django.http import HttpResponse

from budget.models import Entry

def index(request):
    return HttpResponse("Hello, world.")

def entry_list(request):
    template = 'entry_list.html'

    context={
        'entries': Entry.objects.all()
    }

    return render(request, template, context)
