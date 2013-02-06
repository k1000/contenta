# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from yamlfield.fields import YAMLField  # https://github.com/datadesk/django-yamlfield

from services import services
from django.conf import settings

DEFAULT_RENDERER = getattr(settings, "CONTENTA_DEFAULT_RENDERER", 1)


class PageManager(models.Manager):
    def active(self):
        return super(PageManager, self).get_query_set().filter(state=2)

    def siblings(self, page):  # TODO
        if page.parent:
            return self.active().filter(parent__pk=page.parent.pk)

    def same_template(self, template_name):
        return self.active().filter(template_name__exact=template_name)


class Page(models.Model):
    """Page model"""

    objects = PageManager()

    HTML = 1
    TEXTILE = 2
    MARKDOWN = 3
    RESTRUCTUREDTEXT = 4
    RENDER_CHOICES = (
        (HTML, "html"),
        (TEXTILE, "textile"),
        (MARKDOWN, "markdown"),
        (RESTRUCTUREDTEXT, "restructured text"),
    )

    STATES = (
        (1, _("darft")),
        (2, _("published")),
        (3, _("hidden")),
    )
    serv = services  # necessary for admin

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    created_by = models.ForeignKey(User, verbose_name=_("created by"))

    state = models.PositiveSmallIntegerField(_('state'),
        choices=STATES, default=1, db_index=True)

    url = models.CharField(_('URL'),
        blank=True, null=True,
        max_length=100, db_index=True)
    parent = models.ForeignKey("Page",
        related_name='children',
        verbose_name=_("parent"),
        blank=True, null=True,
        db_index=True)

    language = models.CharField(_("language"),
        max_length=3,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE)
    translation_from = models.ForeignKey("Page",
        related_name="translations",
        verbose_name=_("translated from"),
        blank=True, null=True,
        db_index=True,
    )

    title = models.CharField(_("title"), max_length=250)
    slug = models.SlugField(_("Used in the URL of the entry"), max_length=250)
    expert = models.TextField(_("aside"), blank=True, null=True)
    content = models.TextField(_("content"))

    render_with = models.PositiveSmallIntegerField(_('render with'),
                    blank=True,
                    choices=RENDER_CHOICES,
                    default=CONTENTA_DEFAULT_RENDERER)

    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'contenta/contact_page.html'. If this isn't provided, \
        the system will use 'contenta/default.html'."))

    registration_required = models.BooleanField(_('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."))

    variables = YAMLField(_("Variables"),
        blank=True, null=True,
        db_index=True,
        help_text=_("""YAML formated text with variables. http://www.yaml.org/. eg: img:
youtube:
iframe:"""))

    # sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('url',)
        get_latest_by = "publication_date"

    def get_vars(self):
        return self.variables.to_python()

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url

    def get_parents(self):
        # TODO cacheit on root key
        def get_parent(page, parents):
            parent = page.parent
            if parent:
                parents.append(parent)
                return get_parent(parent, parents)
            else:
                return None, parents

        return get_parent(self, [])[1][::-1]

    def get_siblings(self):
        qs = self.__class__._default_manager.using(self._state.db).filter(
            parent__exact=self.parent,
            state__exact=1,
            language__exact=self.language).exclude(pk=self.pk)
        return list(qs)

    def get_translations(self):
        translations = []
        # get other translations from translation source
        if self.translation_from:
            translations.append(self.translation_from)
            translations = translations + list(self.translation_from.translations.exclude(pk=self.pk))

        # get other translations
        translations = translations + list(self.translations.exclude(pk=self.pk))
        return translations

    def save(self, *args, **kwargs):
        if self.parent:
            paret_url = self.parent.url or ""
            self.url = "%s%s/" % (paret_url, self.slug)
        else:
            self.url = "/%s/" % self.slug
        super(Page, self).save(*args, **kwargs)
        children = self.children.all()
        if children:
            for child in children:
                # propagate state to children
                if self.state is 1:
                    child.state = self.state
                child.save()


class Service(models.Model):
    page = models.ForeignKey(Page, related_name="services")
    service = models.SlugField(_("service"), choices=services.list())
    variables = YAMLField(_("Variables"),
        blank=True, null=True,
        db_index=True,
        help_text=_("""YAML formated text with variables. http://www.yaml.org/. eg: img:
youtube:
iframe:"""),
    )
    #weight = models.PositiveSmallIntegerField(_('weight'), default=1)
