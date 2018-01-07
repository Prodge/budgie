import functools

from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden


def dialogflow_auth_required(func):

    @functools.wraps(func)
    def res(request, *args, **kwargs):
        user = authenticate(request=request)
        if not user:
            raise HttpResponseForbidden()
        request.user = user
        func(request, *args, **kwargs)

    return res

