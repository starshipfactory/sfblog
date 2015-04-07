from itertools import islice
from django import template
from django.utils.timezone import now
from schedule.models import Calendar

register = template.Library()


@register.assignment_tag
def get_recent_events(num=5):
    cal = Calendar.objects.get(slug="default")
    occurrences = cal.occurrences_after(now())
    return islice(occurrences, int(num))
