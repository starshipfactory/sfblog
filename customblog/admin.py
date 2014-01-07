# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site

from zinnia.models import Entry
from zinnia.admin import EntryAdmin

from simplecms.admin import ContentAdmin
from simplecms.snippet_editor import AdminSnippetEditor

from customblog.forms import EntryForm


class EntryEditor(AdminSnippetEditor):
    model = Entry
    template_name = 'customblog/admin.html'

    def get_instance_from_content(self, content):
        return content.entry

    def get_content(self, obj):
        if obj is None:
            return None
        return obj.content_ptr

    def get_query_set(self):
        return Entry.objects.all()

    def get_content_initial(self):
        return {'template_slug': 'blog'}

    def save_extra(self, extra_forms, content, adding):
        form = extra_forms['entryform']
        entry = form.save(commit=False)
        entry.content_ptr = content
        entry.save()
        entry.sites.add(Site.objects.get_current())
        form.save_m2m()

    def get_extra_forms(self, instance=None, method="get"):
        initial_data = {}
        if method == "post":
            entryform = EntryForm(self._request.POST, self._request.FILES, instance=instance)
        else:
            entryform = EntryForm(initial=initial_data, instance=instance)
        return {'entryform': entryform}


class MyEntryAdmin(EntryAdmin, ContentAdmin):
    editor = EntryEditor()

admin.site.unregister(Entry)
admin.site.register(Entry, MyEntryAdmin)
