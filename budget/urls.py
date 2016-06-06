from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.home,
        name = 'home'
    ),
    url(
        r'^entry/list/$',
        views.entry_list,
        name = 'entry_list'
    ),
    url(
        r'^entry/(?P<entry_id>\d+)/$',
        views.entry_detail,
        name = 'entry_detail'
    ),
    url(
        r'^entry/(?P<entry_id>\d+)/edit/$',
        views.entry_edit,
        name = 'entry_edit'
    ),
    url(
        r'^entry/create/$',
        views.entry_create,
        name = 'entry_create'
    ),
    url(
        r'^category/create/$',
        views.category_create,
        name = 'category_create'
    ),
]
