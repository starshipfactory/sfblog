from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings

from django.contrib.redirects.models import Redirect


@override_settings(
    APPEND_SLASH=False,
    SITE_ID=1,
)
class RedirectTests(TestCase):

    def setUp(self):
        self.site = Site.objects.get(pk=settings.SITE_ID)
        call_command("simplecms_init", verbosity=0)

    def test_redirect(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial', new_path='/new_target')
        response = self.client.get('/initial')
        self.assertRedirects(response,
            '/new_target', status_code=301, target_status_code=404)

    def test_redirect_with_query_1(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial', new_path='/new_target')
        response = self.client.get('/initial?foo=bar&baz=lala')
        self.assertRedirects(response,
            '/new_target?foo=bar&baz=lala', status_code=301, target_status_code=404)

    def test_redirect_with_query_2(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial', new_path='/new_target?foo=bar')
        response = self.client.get('/initial?baz=lala')
        self.assertRedirects(response,
            '/new_target?foo=bar&baz=lala', status_code=301, target_status_code=404)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_query_3(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial/', new_path='/new_target')
        response = self.client.get('/initial?foo=bar&baz=lala', follow=True)
        self.assertRedirects(response,
            '/new_target/?foo=bar&baz=lala', status_code=301, target_status_code=404)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_query_4(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial/', new_path='/new_target?foo=bar')
        response = self.client.get('/initial?baz=lala', follow=True)
        self.assertRedirects(response,
            '/new_target/?foo=bar&baz=lala', status_code=301, target_status_code=404)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_append_slash(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial/', new_path='/new_target/')
        response = self.client.get('/initial', follow=True)
        self.assertRedirects(response,
            '/new_target/', status_code=301, target_status_code=404)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_append_slash_and_query_string(self):
        Redirect.objects.create(
            site=self.site, old_path='/initial/?foo=bar', new_path='/new_target/')
        response = self.client.get('/initial?foo=bar', follow=True)
        self.assertRedirects(response,
            '/new_target/', status_code=301, target_status_code=404)

    def test_response_gone(self):
        """When the redirect target is '', return a 410"""
        Redirect.objects.create(
            site=self.site, old_path='/initial', new_path='')
        response = self.client.get('/initial')
        self.assertEqual(response.status_code, 410)
