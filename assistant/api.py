import datetime
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from budget.models import Entry

# @login_required
def new_entry(request, category_id):
    assert request.method == 'POST', 'Request must be a POST'

    return JsonResponse({
        'speech': 'Entry has been added',
        'displayText': 'Entry has been added',
        'data': {},
        'contextOut': [],
        'source': "Budgie Money",
    })
