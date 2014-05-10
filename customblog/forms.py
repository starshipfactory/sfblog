# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToManyRel
from django.utils.translation import ugettext_lazy as _

from zinnia.models import Entry, Category
from zinnia.admin.widgets import MPTTFilteredSelectMultiple
from zinnia.admin.fields import MPTTModelMultipleChoiceField


class EntryForm(forms.ModelForm):
    categories = MPTTModelMultipleChoiceField(
        label=_('Categories'), required=False,
        queryset=Category.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('categories'), False,
                                          attrs={'rows': '10'}))

    def __init__(self, *args, **kwargs):
        from django.contrib import admin
        super(EntryForm, self).__init__(*args, **kwargs)
        rel = ManyToManyRel(Category, 'id')
        self.fields['categories'].widget = RelatedFieldWidgetWrapper(
            self.fields['categories'].widget, rel, admin.site)
        self.fields['tags'].help_text = u"Kommagetrennt"
        #self.fields['image'].help_text = u"764px breit, 300px hoch;"\
        #    u" falls größer, wird zentral geschnitten"

    class Meta:
        model = Entry
        fields = ['title', 'slug', 'resized_image', 'status', 'categories',
                  'tags', 'comment_enabled']
