import json

from datetime import datetime

from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from budget.models import Entry, Category

@login_required
@csrf_exempt
def new_entry(request):
    assert request.method == 'POST', 'Request must be a POST'

    body = json.loads(request.body.decode('utf-8'))

    raw_query = body['originalRequest']['data']['inputs'][0]['arguments'][0]['rawText']
    parameters = body['result']['parameters']

    entry = Entry(
        label = parameters['category'],
        value = parameters['unit-currency']['amount'],
        date = datetime.strptime(body['result']['parameters']['date'], '%Y-%m-%d'),
        flow_type = parameters['flow_type'],
        category = Category.objects.get(name__iexact=parameters['category']),
        user = request.user,
    )
    entry.save()

    return JsonResponse({
        'speech': 'Entry for {} of {} has been added'.format(entry.value, entry.label),
        'displayText': 'Entry for {} of {} has been added'.format(entry.value, entry.label),
        'data': {},
        'contextOut': [],
        'source': "Budgie Money",
    })
