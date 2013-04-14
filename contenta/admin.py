import os

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from models import Page, Service
from services import services

from settings import *


def get_template_names():
    templates = []
    tmpl_dir = os.path.join(settings.TEMPLATE_DIRS[0], "contenta")
    os.chdir(tmpl_dir)
    return templates + ["contenta/%s" % files for files in os.listdir(".") if files.endswith(".html")]


def page_choices(instance):
    """
    excluded self
    """
    return Page.objects.exclude(pk=instance.pk)


class ContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        # protect that page can asign self as parent or source of translation
        self.fields['parent'].queryset = page_choices(self.instance)
        self.fields['translation_from'].queryset = page_choices(self.instance)

    class Meta:
        model = Page


class ServiceForm(forms.ModelForm):
    service = forms.ChoiceField(label="Service",
            choices=services.list())

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].choices = [("", "------")] + services.list()

    def clean(self):
        cleaned_data = super(ServiceForm, self).clean()
        serv = cleaned_data.get("service")
        dat = services.services[serv][1]
        if "clean" in dat:
            variables = cleaned_data.get("variables")
            clean = dat["clean"](variables)
            if clean:
                raise forms.ValidationError(clean)
        return cleaned_data

    class Meta:
        model = Service


class ServiceInline(admin.TabularInline):
    form = ServiceForm
    model = Service
    extra = 1


class ContentAdmin(admin.ModelAdmin):
    form = ContentForm

    fieldsets = (
        (None, {'fields': [
            ('url', 'parent'),
            'state',
            ('language', 'translation_from'),
            ('created_by', 'created_at', 'modified_at', )]}),
        (None, {'fields': ('title', 'slug', ('menu_title', 'weight'), 'img', 'expert', 'content')}),
        (_('Advanced options'),
            {'classes': ('collapse',),
            'fields': ('registration_required', 'render_with', 'template_name', 'variables')}
        ),
    )
    readonly_fields = ('url', 'created_by', 'created_at', 'modified_at')
    list_display = ['url', 'title', 'language', 'state', 'created_at']
    list_filter = ['registration_required', "state", "language"]
    search_fields = ['url', 'title']
    prepopulated_fields = {"slug": ("title",)}

    if MULTISITE:
        fieldsets[0][1]['fields'].insert(1, 'sites')
        list_filter.append("sites")

    exclude = ("created_by",)
    inlines = (ServiceInline, )

    save_as = True

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['available_templates'] = get_template_names()
        extra_context['services'] = services
        return super(ContentAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        css = {"all": ("css/admin.css",)}
        js = ["js/admin.js", "ckeditor/ckeditor.js"]
        if FILEBROWSER_URL:
            js.append(FILEBROWSER_URL)

admin.site.register(Page, ContentAdmin)
