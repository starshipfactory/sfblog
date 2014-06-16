from itertools import islice
from django.template import Library

from tagging.models import Tag
from tagging.utils import calculate_cloud

from zinnia.models.entry import Entry

register = Library()


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def core_get_tag_cloud(context, steps=6, min_count=None, max_num_tags=2,
                       template='zinnia/tags/tag_cloud.html'):
    """
    Return a cloud of published tags.
    """
    tags = Tag.objects.usage_for_queryset(
        Entry.published.all(), counts=True,
        min_count=min_count)
    tags = sorted(tags, key=lambda t: t.count, reverse=True)
    tags = list(islice(tags, max_num_tags))
    return {'template': template,
            'tags': calculate_cloud(tags, steps),
            'context_tag': context.get('tag')}
