from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext, Template
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from models import Page, services
from settings import *


def markup(txt, markupname=0):
    if markupname is Page.TEXTILE:
        from django.contrib.markup.templatetags.markup import textile
        return textile(txt)
    elif markupname is Page.MARKDOWN:
        from django.contrib.markup.templatetags.markup import markdown
        return markdown(txt)
    elif markupname is Page.RESTRUCTUREDTEXT:
        from django.contrib.markup.templatetags.markup import restructuredtext
        return restructuredtext(txt)
    else:
        return txt


def page(request, url):
    """

    """
    vars = Context(request)

    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(Page, url__exact=url, state__in=[2, 4])
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)

    lang = f.language
    translation.activate(lang)
    request.session['django_language'] = lang

    cur_vars = f.variables
    if cur_vars:
        vars.update(cur_vars)

    page_services = f.services.all()
    if page_services:
        for service in page_services:
            cur_service = services.get(service.service)

            if cur_service:
                cur_vars = cur_service[0](request, service.variables)

                # shortcircut return for redirect etc
                if isinstance(cur_vars, HttpResponse):
                    return cur_vars

                vars.update(cur_vars)

    # if we have services or/and variables we will evaluate content
    if page_services and cur_vars:
        t = Template(f.content)
        content_vars = RequestContext(request, vars)
        f.content_rndr = mark_safe(t.render(content_vars))
    else:
        f.content_rndr = f.content

    # render html acording to markup
    f.content_rndr = markup(f.content_rndr, f.render_with)
    vars.update({"page": f})
    return vars


def render_page(request, url):

    context = page(request, url)
    if type(context) is Context:
        return render(request,
                context['page'].template_name or DEFAULT_TEMPLATE, context)
    else:
        return context


@staff_member_required
def render_json(request, url):
    from django.core import serializers

    context = page(request, url)
    if type(context) is Context:
        json = serializers.serialize('json', [context['page']])
    else:
        json = [{"title": "Page has redirect. Nothing to show"}]

    return HttpResponse(json, mimetype='application/json')


@staff_member_required
def save_content(request, url):
    if request.method == "POST":
        content = request.POST.get("content")
        page = Page.objects.get(url__exact=url)
        page.content = content
        page.save()
        success = True
    else:
        success = False

    return HttpResponse([{"success": success}], mimetype='application/json')
