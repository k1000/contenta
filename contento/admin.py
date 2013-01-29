from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Page, Service
from services import services
from django.conf import settings


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

    # translation_from = forms.ModelChoiceField(
    #     queryset=Page.objects.exclude(pk=1),
    # )
    #queryset=Area.objects.exclude(area=None)
    # url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
    #     help_text=_("Example: '/about/contact/'. Make sure to have leading"
    #                   " and trailing slashes."),
    #     error_message=_("This value must contain only letters, numbers,"
    #                       " dots, underscores, dashes, slashes or tildes."))

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

    fieldsets = (
        (None,
            {'fields': (('created_at', 'created_by'), 'modified_at', )}
        ),
        (None, {'fields': (
            ('url', 'parent'),
            'sites',
            'state',
            ('language', 'translation_from'))}),
        (None, {'fields': ('title', 'slug', 'expert', 'content')}),
        (_('Advanced options'),
            {'classes': ('collapse',),
            'fields': ('registration_required', 'render_with', 'template_name', 'variables')}
        ),
    )
    readonly_fields = ('url', 'created_by', 'created_at', 'modified_at')
    list_display = ('url', 'title', 'language', 'state', 'created_at')
    list_filter = ('sites', 'registration_required', "state", "language")
    search_fields = ['url', 'title']
    prepopulated_fields = {"slug": ("title",)}

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
