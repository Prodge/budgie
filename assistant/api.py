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


def get_total_expense_over_range(user, start_date, end_date, category=None):
    return get_total_value(
        Entry.objects.filter(
            user = user,
            date__gte = start_date,
            date__lte = end_date,
            category = category,
        )
    )


def cast_dialogflow_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')


def expense_query(request, body={}, parameters={}, **kwargs):
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
    dollars, cents = map(int, '{0:.2f}'.format(total_spent).split('.'))

    date_period_user_string = body['result']['contexts'][0]['parameters']['date-period.original']
    date_user_string = body['result']['contexts'][0]['parameters']['date.original']

    def get_dollars_and_cents_string(dollars, cents):
        if dollars and cents:
            return '{} dollars and {} cents'.format(dollars, cents)
        if dollars:
            return '{} dollars'
        if cents:
            return '{} cents'
        if dollars == 0 and cents == 0:
            return 'nothing'
        return ''

    response_text = 'You spent {} {} {} {}'.format(
        get_dollars_and_cents_string(dollars, cents),
        'on {}'.format(category.name) if category else '',
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

