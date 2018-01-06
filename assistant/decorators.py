import functools

from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden


def dialogflow_auth_required(func):

    @functools.wraps(func)
    def res(request, *args, **kwargs):
        if not authenticate(request=request):
            raise HttpResponseForbidden()
        func(request, *args, **kwargs)

    return res

