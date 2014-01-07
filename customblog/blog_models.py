from django.db import models
from zinnia.models_bases.entry import AbstractEntry

from simplecms.models import Content


class BlogEntry(AbstractEntry):
    content_ptr = models.OneToOneField(Content)

    class Meta(AbstractEntry.Meta):
        abstract = True
