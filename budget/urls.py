from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.home,
        name = 'home'
    ),
    url(
        r'^entry-list/',
        views.entry_list,
        name = 'entry_list'
    ),
    url(
        r'^entry/(?P<pk>\d+)/',
        views.entry_edit,
        name = 'entry_edit'
    ),
    url(
        r'^entry-create/',
        views.entry_create,
        name = 'entry_create'
    ),
]
