from schedule.models import Event
from schedule.utils import EventListManager
from django.utils.timezone import now

es = Event.objects.all()
print list(EventListManager(es).occurrences_after(now()))
