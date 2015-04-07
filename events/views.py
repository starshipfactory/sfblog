from itertools import islice
from django.views.generic import ListView
from django.utils.timezone import now
from schedule.models import Calendar


class EventList(ListView):
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        cal = Calendar.objects.get(slug="testkalender")
        occurrences = cal.occurrences_after(now())
        return islice(occurrences, 10)
