from django.conf.urls import url

from . import api

urlpatterns = [
    url(
        r'^api/v1/assistant$',
        api.router,
        name = 'assistant_api'
    ),
]
