from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=128)
    page = models.ForeignKey("simplecms.Page", blank=True, null=True)

    def __unicode__(self):
        return self.name


class EventDescription(models.Model):
    cost = models.TextField(default="", blank=True)
    page = models.ForeignKey("simplecms.Page", blank=True, null=True)
    post = models.ForeignKey("zinnia.Entry", blank=True, null=True)
    location = models.ForeignKey(Location)
    instructor = models.CharField(max_length=128)
    event = models.OneToOneField("schedule.Event")

    def __unicode__(self):
        return self.event.title

    def get_absolute_url(self):
        try:
            return self.post.get_absolute_url()
        except:
            pass
        try:
            return self.page.get_absolute_url()
        except:
            pass
"""
list(rrule(dateutil.rrule.MONTHLY, count=5,
        byweekday=dateutil.rrule.FR,
        dtstart=datetime.date(2015,4,3),
        bysetpos=1))

=>

byweekday:4;bysetpos:1
"""
