from django.conf.urls import url

from . import api

urlpatterns = [
    url(
        r'^api/v1/new-entry$',
        api.new_entry,
        name = 'assistant_api_new_entry'
    ),
]
