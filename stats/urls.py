from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.stats_home,
        name = 'stats_home'
    ),
]
