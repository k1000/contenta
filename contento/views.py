from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template import Context, Template
from django.conf import settings
from django.utils.translation import get_language
from django.utils.safestring import mark_safe
from django.shortcuts import render


from transmeta import get_real_fieldname

from models import Page, services

DEFAULT_TEMPLATE = 'contento/default.html'


def markup(txt, markupname=""):
    if markupname is Page.TEXTILE:
        from django.markup import textile
        return textile(txt)
    elif markupname is Page.MARKDOWN:
        from django.markup import markdown
        return markdown(txt)
    elif markupname is Page.RESTRUCTUREDTEXT:
        from django.markup import restructuredtext
        return restructuredtext(txt)
    else:
        return txt


def page(request, url):
    """

    """
    vars = Context()
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(Page, url__exact=url, sites__id__exact=settings.SITE_ID, state__exact=2)
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)

    lang = get_language()
    content_local = get_real_fieldname("content", lang)

    page_services = f.services.all()
    if page_services:
        for service in page_services:
            cur_service = services.get(service.service)

            # shortcircut return for redirect etc
            if "return" in cur_service[1]:
                return cur_service[0](request, service.variables)

            cur_vars = cur_service[0](request, service.variables)

            # default variables for current language
            if lang in cur_vars:
                vars.update(cur_vars[lang])
            else:
                vars.update(cur_vars)

        t = Template(content_local)
        f.content_rndr = mark_safe(t.render(vars))
    else:
        f.content_rndr = getattr(f, content_local)

    # render html acording to markup
    markup_name = Page.MARKUP_CHOICES[f.render_with - 1][1]
    f.content_rndr = markup(f.content_rndr, markup_name)
    vars.update({"page": f})
    return render(request, f.template_name or DEFAULT_TEMPLATE, vars)
