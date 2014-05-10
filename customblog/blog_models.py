from django.db import models
from django.utils.translation import ugettext_lazy as _
from zinnia.models_bases.entry import AbstractEntry
from zinnia.settings import UPLOAD_TO

from simplecms.models import Content
from imagetools.models import ThumbnailField


class BlogEntry(AbstractEntry):
    content_ptr = models.OneToOneField(Content)
    resized_image = ThumbnailField(
        _('image'), blank=True, default='', upload_to=UPLOAD_TO,
        sizes=[(647, 0, False, "blogtitle")],
        help_text=_('Used for illustration'))

    class Meta(AbstractEntry.Meta):
        abstract = True
