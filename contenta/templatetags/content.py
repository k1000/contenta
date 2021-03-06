from django import template
from django.utils.translation import ugettext as _
from django.conf import settings

from contenta.models import Page

register = template.Library()


class PageNode(template.Node):
    def __init__(self, context_name, starts_with=None, user=None):
        self.context_name = context_name
        if starts_with:
            self.starts_with = template.Variable(starts_with)
        else:
            self.starts_with = None
        if user:
            self.user = template.Variable(user)
        else:
            self.user = None

    def render(self, context):
        pages = Page.objects.filter(sites__id=settings.SITE_ID)
        # If a prefix was specified, add a filter
        if self.starts_with:
            pages = pages.filter(
                url__startswith=self.starts_with.resolve(context))

        # If the provided user is not authenticated, or no user
        # was provided, filter the list to only public flatpages.
        if self.user:
            user = self.user.resolve(context)
            if not user.is_authenticated():
                pages = pages.filter(registration_required=False)
        else:
            pages = pages.filter(registration_required=False)

        context[self.context_name] = pages
        return ''


def get_pages(parser, token):
    """
    Retrieves all pages objects available for the current site and
    visible to the specific user (or visible to all users if no user is
    specified). Populates the template context with them in a variable
    whose name is defined by the ``as`` clause.

    An optional ``for`` clause can be used to control the user whose
    permissions are to be used in determining which pages are visible.

    An optional argument, ``starts_with``, can be applied to limit the
    returned flatpages to those beginning with a particular base URL.
    This argument can be passed as a variable or a string, as it resolves
    from the template context.

    Syntax::

        {% get_pages ['url_starts_with'] [for user] as context_name %}

    Example usage::

        {% get_pages as pages %}
        {% get_pages for someuser as pages %}
        {% get_pages '/about/' as about_pages %}
        {% get_pages prefix as about_pages %}
        {% get_pages '/about/' for someuser as about_pages %}
    """
    bits = token.split_contents()
    syntax_message = _("%(tag_name)s expects a syntax of %(tag_name)s "
                       "['url_starts_with'] [for user] as context_name" %
                       dict(tag_name=bits[0]))
   # Must have at 3-6 bits in the tag
    if len(bits) >= 3 and len(bits) <= 6:

        # If there's an even number of bits, there's no prefix
        if len(bits) % 2 == 0:
            prefix = bits[1]
        else:
            prefix = None

        # The very last bit must be the context name
        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[-1]

        # If there are 5 or 6 bits, there is a user defined
        if len(bits) >= 5:
            if bits[-4] != 'for':
                raise template.TemplateSyntaxError(syntax_message)
            user = bits[-3]
        else:
            user = None

        return PageNode(context_name, starts_with=prefix, user=user)
    else:
        raise template.TemplateSyntaxError(syntax_message)


class MenuNode(template.Node):
    def __init__(self, context_name, root_url, lang=None):
        self.context_name = context_name
        # if root_url:
        #     self.root_url = template.Variable(starts_with)
        # else:
        #     self.starts_with = None
        # if user:
        #     self.lang = template.Variable(user)
        # else:
        #     self.user = None

    def render(self, context):
        
        return ''


def get_menu(parser, token):
    """
    
    """

register.tag('get_menu', get_menu)
register.tag('get_pages', get_pages)
