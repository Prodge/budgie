import json

from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from budget.models import Entry, Category

# @login_required
@csrf_exempt
def new_entry(request):
    assert request.method == 'POST', 'Request must be a POST'

    body = json.loads(request.body.decode('utf-8'))

    raw_query = body['originalRequest']['data']['inputs'][0]['arguments'][0]['rawText']
    parameters = body['result']['parameters']

    entry = Entry(
        label = paramaters['category'],
        value = parameters['unit-currency']['amount'],
        date = datetime.strptime(body['result']['parameters']['date'], '%Y-%m-%d'),
        flow_type = parameters['flow_type'],
        category = Category.objects.get(name__iexact=paramaters['category']),
        User = User.objects.get(username='tim'),
    )
    entry.save()

    return JsonResponse({
        'speech': 'Entry for {} of {} has been added'.format(entry.value),
        'displayText': 'Entry for {} of {} has been added'.format(entry.label),
        'data': entry.__dict__,
        'contextOut': [],
        'source': "Budgie Money",
    })
