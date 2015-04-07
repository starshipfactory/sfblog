from django.contrib import admin
from schedule.models import Event
import schedule.admin  # NOQA
from events.models import EventDescription, Location


class EventDescriptionInline(admin.StackedInline):
    model = EventDescription


class EventAdmin(admin.ModelAdmin):
    inlines = [EventDescriptionInline]
    fields = ["start", "end", "title", "rule",
              "end_recurring_period", "calendar"]
admin.site.unregister(Event)
admin.site.register(Event, EventAdmin)


admin.site.register(Location)
