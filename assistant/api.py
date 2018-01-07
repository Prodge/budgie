import json

from datetime import datetime

from oauth2_provider.models import AccessToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from budget.models import Entry, Category
from budget.views import get_total_value
from assistant.decorators import dialogflow_auth_required


@dialogflow_auth_required
@csrf_exempt
def router(request):
    assert request.method == 'POST', 'Request must be a POST'

    body = json.loads(request.body.decode('utf-8'))
    parameters = body['result']['parameters']
    raw_query = body['originalRequest']['data']['inputs'][0]['arguments'][0]['rawText']

    return {
        'new_entry': new_entry,
        'expense_query': expense_query,
    }[body['result']['metadata']['intentName']](
        request,
        body=body,
        parameters=parameters,
        raw_query=raw_query
    )


def new_entry(request, parameters=[], **kwargs):

    entry = Entry(
        label = parameters['label'],
        value = parameters['unit-currency']['amount'],
        date = cast_dialogflow_date(parameters['date']),
        flow_type = parameters['flow_type'],
        category = Category.objects.get(name__iexact=parameters['category']),
        user = request.user,
        description = parameters['description'],
    )
    entry.save()

    return JsonResponse({
        'speech': 'Entry for {} of {} has been added'.format(entry.value, entry.label),
        'displayText': 'Entry for {} of {} has been added'.format(entry.value, entry.label),
        'data': {},
        'contextOut': [],
        'source': "Budgie Money",
    })


def get_total_expense_over_range(user, start_date, end_date):
    return get_total_value(
        Entry.objects.get(
            user = user,
            date__gte = start_date,
            date__lte = end_date,
        )
    )


def cast_dialogflow_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')


def expense_query(request, parameters=[], **kwargs):
    try:
        category = Category.objects.get(name__iexact=parameters['category'])
    except Category.DoesNotExist:
        category = None

    if parameters.get('date'):
        start_date = end_date = cast_dialogflow_date(parameters['date'])

    if parameters.get('date-period'):
        start_date, end_date = map(cast_dialogflow_date, parameters.get('date-period').split('/'))

    total_spent = get_total_expense_over_range(
        request.user,
        start_date,
        end_date
    )

    date_period_user_string = body['result']['contexts'][0]['date-period.original']
    date_user_string = body['result']['contexts'][0]['date.original']

    response_text = 'You spent {} {} {} {}'.format(
        total_spent,
        'on {}'.format(caterogy.name) if category else '',
        'over {}'.format(date_period_user_string),
        date_user_string
    )

    return JsonResponse({
        'speech': response_text,
        'displayText': response_text,
        'data': {},
        'contextOut': [],
        'source': "Budgie Money",
    })

