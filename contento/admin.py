from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from transmeta import canonical_fieldname
from models import Page
from django.conf import settings


class ContentForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
        help_text=_("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message=_("This value must contain only letters, numbers,"
                          " dots, underscores, dashes, slashes or tildes."))

    class Meta:
        model = Page


class ContentAdmin(admin.ModelAdmin):
    form = ContentForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [(None, {'fields': ('url', 'sites', 'state')})]
        for lang in settings.PAGE_LANGUAGES:
            fieldsets.append((lang[1], {'classes': (lang[0], 'tab'),
                'fields': ('title_%s' % lang[0], 'expert_%s' % lang[0], 'content_%s' % lang[0],)}))
        fieldsets.append((_('Advanced options'),
            {'classes': ('collapse',),
            'fields': ("variables", 'registration_required', "render_with", 'template_name')}))
        return fieldsets

    list_display = ('url', 'title', 'state', 'created_at')
    list_filter = ('sites', 'registration_required', "state")
    search_fields = ('url', 'title')
    exclude = ("created_by",)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    class Media:
        css = {"all": ("css/tabs.css",)}
        js = ("js/tabs.js", "ckeditor/ckeditor.js", "filebrowser/js/FB_CKEditor.js")

#admin.site.register(ContentAdmin, ContentForm)
admin.site.register(Page, ContentAdmin)
