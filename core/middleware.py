from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import get_current_site
from django.utils.http import urlparse
from django import http


class RedirectFallbackPassQuery(object):
    """
    Variant of django.contrib.redirects.middleware.RedirectFallbackMiddleware
    that ignores the query string when looking for a Redirect object, then
    appends it to the new path.

    Put this *before* the original RedirectFallbackMiddleware, because we
    only want to handle the cases not handled by RedirectFallbackMiddleware.
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response

        full_path = request.get_full_path()
        parsed_path = urlparse(full_path)
        path_without_query = parsed_path.path
        current_site = get_current_site(request)

        r = None
        try:
            r = Redirect.objects.get(site=current_site, old_path=path_without_query)
        except Redirect.DoesNotExist:
            pass
        if settings.APPEND_SLASH and not request.path.endswith('/'):
            # Try appending a trailing slash.
            path_without_query = path_without_query + "/"
            try:
                r = Redirect.objects.get(site=current_site, old_path=path_without_query)
            except Redirect.DoesNotExist:
                pass
        if r is not None:
            if r.new_path == '':
                return http.HttpResponseGone()
            # preserve query string
            dest = "%s%s%s" % (r.new_path, ('?' in r.new_path and '&' or '?'), parsed_path.query)
            return http.HttpResponsePermanentRedirect(dest)

        # No redirect was found. Return the response.
        return response
