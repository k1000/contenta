from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template import Context, Template
from django.conf import settings
from django.utils.translation import get_language
from django.utils.safestring import mark_safe
from django.shortcuts import render

from transmeta import get_real_fieldname

from models import Page

DEFAULT_TEMPLATE = 'contento/default.html'


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
    vars = {}
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

    # TODO
    # # apply variables to content
    lang = get_language()
    content_local = get_real_fieldname("content", lang)
    if f.variables:
        vars.update(f.variables)

        # default variables for current language
        if lang in f.variables:
            f.update(f.variables[lang])

        t = Template(content_local)
        f.content_rndr = mark_safe(t.render(Context(f.variables)))
    else:
        f.content_rndr = getattr(f, content_local)

    # render html acording to markup
    markup_name = Page.MARKUP_CHOICES[f.render_with]
    f.content_rndr = markup(f.content_rndr, markup_name)
    vars.update({"page": f})
    return render(request, f.template_name or DEFAULT_TEMPLATE, vars)
