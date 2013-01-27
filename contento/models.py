# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from transmeta import TransMeta
from yamlfield.fields import YAMLField  # https://github.com/datadesk/django-yamlfield

from services import services
from django.conf import settings


class Page(models.Model):
    """Registry model"""
    __metaclass__ = TransMeta
    HTML = 1
    TEXTILE = 2
    MARKDOWN = 3
    RESTRUCTUREDTEXT = 4
    MARKUP_CHOICES = (
        (HTML, "html"),
        (TEXTILE, "textile"),
        (MARKDOWN, "markdown"),
        (RESTRUCTUREDTEXT, "restructured text"),
    )

    STATES = (
        (1, _("darft")),
        (2, _("published"))
    )
    serv = services  # necessary for admin

    #if settings.content.tree:
    parent = models.ForeignKey("Page",
        verbose_name=_("parent"),
        blank=True, null=True,
        db_index=True,
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    created_by = models.ForeignKey(User, verbose_name=_("created by"))
    state = models.PositiveSmallIntegerField(_('state'),
        choices=STATES, default=1, db_index=True)
    url = models.CharField(_('URL'), max_length=100, db_index=True)

    title = models.CharField(_("title"), max_length=250)
    expert = models.TextField(_("aside"), blank=True, null=True)
    content = models.TextField(_("content"))

    render_with = models.PositiveSmallIntegerField(_('render with'),
                    blank=True,
                    choices=MARKUP_CHOICES,
                    default=1)

    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'contento/contact_page.html'. If this isn't provided, \
        the system will use 'contento/default.html'."))

    registration_required = models.BooleanField(_('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."))

    variables = YAMLField(_("Variables"),
        blank=True, null=True,
        db_index=True,
        help_text=_("""YAML formated text with variables. http://www.yaml.org/. eg: img:
youtube:
iframe:"""))

    sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('url',)
        translate = ('title', 'content', 'expert')

    def get_vars(self):
        return self.variables.to_python()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


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
