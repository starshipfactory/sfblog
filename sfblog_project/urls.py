import re
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from zinnia.sitemaps import TagSitemap, AuthorSitemap, CategorySitemap, EntrySitemap
from simplecms.sitemap import PageSitemap

sitemaps = {
    'tags': TagSitemap(),
    'authors': AuthorSitemap(),
    'categories': CategorySitemap(),
    'entries': EntrySitemap(),
    'pages': PageSitemap(),
}


urlpatterns = patterns(
    '',
    url(r'', include('zinnia.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns(
        '',
        url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
            'django.contrib.staticfiles.views.serve'),
    )

urlpatterns += patterns(
    '',
    url(r'', include("simplecms.urls")),
)
