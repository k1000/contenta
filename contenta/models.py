# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# from django.core.cache import cache


from yamlfield.fields import YAMLField  # https://github.com/datadesk/django-yamlfield

from services import services
from settings import *
from manager import PageManager


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
        (4, _("hidden from menu")),
    )

    serv = services  # necessary for admin

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    created_by = models.ForeignKey(User, verbose_name=_("created by"))

    state = models.PositiveSmallIntegerField(_('state'),
        choices=STATES, default=1, db_index=True)

    url = models.CharField(_('URL'),
        unique=True,
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
        help_text=_("points to the page which is the source of curent translation")
    )

    title = models.CharField(_("title"), max_length=250)
    menu_title = models.CharField(_("menu title"), max_length=30,
        help_text=_('used in menus'))
    weight = models.PositiveSmallIntegerField(_('menu weight'),
        default=1, db_index=True,
        help_text=_('determinates order in menu. Beiger weight = higher position in menu'))

    slug = models.SlugField(_("identificator"), max_length=250,
        help_text=_('Used to build URL string'))
    expert = models.TextField(_("expert"),
            blank=True, null=True,
            help_text=_('page expert or quote')
    )
    img = models.ImageField(_("main image"),
        blank=True, null=True,
        upload_to="uploads/contenta")

    content = models.TextField(_("content"))

    render_with = models.PositiveSmallIntegerField(_('render with'),
                    blank=True,
                    choices=RENDER_CHOICES,
                    default=DEFAULT_RENDERER)

    template_name = models.CharField(_('template name'),
        max_length=70, blank=True,
        help_text=_("Example: 'contenta/contact_page.html'. If this isn't provided, \
        the system will use 'contenta/default.html'."))

    registration_required = models.BooleanField(_('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."))

    variables = YAMLField(_("Variables"),
        blank=True, null=True,
        db_index=True,
        help_text=HELP_TXT_YAML)

    if MULTISITE:
        sites = models.ManyToManyField(SITE_MODEL)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('url',)
        get_latest_by = "publication_date"

    @classmethod
    def active_pages_dict(cls, **filter):
        return dict(cls.objects.active().values_list("url", "title", "parent__url"))

    def get_parents_from_url(self, url=None):
        return (url or self.url).split("/")[1:-2]

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url

    def get_root(self):
        """get root page based on first url element"""

        def _get_root(self):
            parent_slugs = self.url.split("/")[1:-1]
            if len(parent_slugs) == 1:
                return self
            else:
                return Page.objects.get(slug=parent_slugs[0])

        self._root = getattr(self, "_root", _get_root(self))
        return self._root

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

    def get_descendants(self, language=None, conditions=None):
        """"""

        def get_childern(page, descendants):
            children = page.children.filter(state__exact=2).order_by('-weight', 'menu_title')
            if children:
                kids = []
                for child in children:
                    kids.append(get_childern(child, descendants))
                return [page, kids]
            else:
                return [page, []]

        descendants = get_childern(self, [])
        return descendants[1]

    def get_siblings(self):
        qs = self.__class__._default_manager.using(self._state.db).filter(
            parent__exact=self.parent,
            state__exact=1,
            language__exact=self.language).exclude(pk=self.pk)

        return list(qs)

    def is_root(self):
        """Return ``True`` if the page is the root page."""
        return not self.parent

    def get_translations(self):
        translations = []
        # get other translations from translation source
        if self.translation_from:
            translations.append(self.translation_from)
            translations += list(self.translation_from.translations.exclude(pk=self.pk))

        # get other translations
        translations += list(self.translations.exclude(pk=self.pk))
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
    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        #self._meta.get_field_by_name('service')[0]._choices = services.list()

    page = models.ForeignKey(Page, related_name="services")
    service = models.SlugField(_("service"))
    variables = YAMLField(_("Parameters"),
        blank=True, null=True,
        db_index=True,
        help_text=HELP_TXT_YAML,
    )
    #weight = models.PositiveSmallIntegerField(_('weight'), default=1)
