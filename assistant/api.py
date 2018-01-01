import datetime
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from budget.models import Entry

# @login_required
@csrf_exempt
def new_entry(request):
    assert request.method == 'POST', 'Request must be a POST'

    return JsonResponse({
        'speech': 'Entry has been added',
        'displayText': 'Entry has been added',
        'data': {},
        'contextOut': [],
        'source': "Budgie Money",
    })
