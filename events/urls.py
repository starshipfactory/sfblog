from django.conf.urls import patterns, url
from events.views import EventList


urlpatterns = patterns(
    '',
    url(
        regex='^$',
        view=EventList.as_view(),
        name='events-list',
    ),
)
