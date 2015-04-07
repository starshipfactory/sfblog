from itertools import islice
from django.views.generic import ListView
from django.utils.timezone import now
from schedule.models import Calendar


class EventList(ListView):
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_calendar(self):
        return Calendar.objects.get(slug="default")

    def get_context_data(self, **kwargs):
        ctx = super(EventList, self).get_context_data(**kwargs)
        ctx['cal'] = self.get_calendar()
        return ctx

    def get_queryset(self):
        cal = self.get_calendar()
        occurrences = cal.occurrences_after(now())
        return islice(occurrences, 25)
