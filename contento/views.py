from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import get_language
from django.shortcuts import render

from models import Page

DEFAULT_TEMPLATE = 'flatpage/default.html'


def markup(txt, markupname=""):
    if markupname is Page.TEXTILE:
        import textile
        return textile.textile(txt)
    elif markupname is Page.MARKDOWN:
        import markdown
        return markdown.markdown(txt)
    elif markupname is Page.RESTRUCTUREDTEXT:
        from docutils.core import publish_parts
        return publish_parts(txt)
    else:
        return txt


def page(request, url):
    """

    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(Page, url__exact=url, sites__id__exact=settings.SITE_ID)
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    # Serve the content in the language defined by the Django translation module
    # if possible else serve the default language.
    f._default_language = get_language()

    variables = f.variables.to_python()

    # default variables for current language
    if f._default_language in variables:
        f.update(variables[f._default_language])

    # apply variables to content
    if f.variables:
        f.content = render_to_string(f.content, )

    # render html acording to markup
    markup_name = Page.MARKUP_CHOICES[f.render_with]
    f.content = markup(f.content, markup_name)

    return render(request, f.template_name or DEFAULT_TEMPLATE, f)
