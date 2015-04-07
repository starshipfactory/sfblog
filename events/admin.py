# -*- encoding: utf-8 -*-
from django.contrib import admin
from django import forms
from schedule.models import Event
import schedule.admin  # NOQA
from events.models import EventDescription, Location


class EventDescAdminForm(forms.ModelForm):
    class Meta:
        model = EventDescription

    def clean(self):
        cd = super(EventDescAdminForm, self).clean()
        if cd['page'] is None and cd['post'] is None:
            raise forms.ValidationError(
                u"Bitte Page oder Post auswählen")
        return cd


class EventDescriptionInline(admin.StackedInline):
    model = EventDescription
    form = EventDescAdminForm


class EventAdmin(admin.ModelAdmin):
    inlines = [EventDescriptionInline]
    save_on_top = True
    fields = ["start", "end", "title", "rule",
              "end_recurring_period", "calendar"]
admin.site.unregister(Event)
admin.site.register(Event, EventAdmin)


admin.site.register(Location)
