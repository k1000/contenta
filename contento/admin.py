from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Page, Service
from services import services
from django.conf import settings


class ContentForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
        help_text=_("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message=_("This value must contain only letters, numbers,"
                          " dots, underscores, dashes, slashes or tildes."))

    class Meta:
        model = Page


class ServiceForm(forms.ModelForm):
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = [(None, {'fields': (('url', 'parent'), 'sites', 'state')})]
        for lang in settings.LANGUAGES:
            fieldsets.append((lang[1], {'classes': (lang[0], 'tab'),
                'fields': ('title_%s' % lang[0], 'expert_%s' % lang[0], 'content_%s' % lang[0],)}))
        fieldsets.append((_('Advanced options'),
            {'classes': ('collapse',),
            'fields': ('registration_required', 'render_with', 'template_name')}))
        return fieldsets

    list_display = ('url', 'title', 'state', 'created_at')
    list_filter = ('sites', 'registration_required', "state")
    search_fields = ['url']
    for lang in settings.LANGUAGES:
        search_fields.append("title_%s" % lang[0])

    exclude = ("created_by",)
    inlines = (ServiceInline, )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    class Media:
        css = {"all": ("css/tabs.css",)}
        js = ["js/tabs.js", "ckeditor/ckeditor.js"]
        if "filebrowser" in settings.INSTALLED_APPS:
            js.append("filebrowser/js/FB_CKEditor.js")


#admin.site.register(ContentAdmin, ContentForm)
admin.site.register(Page, ContentAdmin)
