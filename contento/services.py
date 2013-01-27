# -*- coding: utf-8 -*-
from django.conf import settings


class Services():
    services = dict()

    def register(self, identicator, service, kwargs=None):
        self.services[identicator] = [service, kwargs]

    def unregister(self, identicator):
        del(self.services[identicator])

    def list(self):
        return zip(self.services.keys(), self.services.keys())

    def get(self, identicator):
        if identicator in self.services:
            return self.services[identicator]
        else:
            KeyError  # TODO protect from refering of non registered services


# very simple service just takes variables from input and injects them to the template
def enviroment(request, data):
    return data


def redirect(request, data):
    from django.http import HttpResponseRedirect
    if not "url" in data or data["url"] is None:
        if not settings.DEBUG:
            return {}
    return HttpResponseRedirect(data.get("url"))


def get_pages(request, data):
    from models import Page
    pages = Page.objects.filter(**data.get("filter"))
    return pages


def clean_page(data):
    if not "filter" in data:
        return "You must have filter keyword. See django docs for queries"
    else:
        return None


def clean_redirect(data):
    if not "url" in data:
        return "You must indicate url to redirect. ex: url: '/admin/'"
    else:
        return None

services = Services()

services.register("enviroment",
        enviroment,
        {"desc": "variables are added to the context of the template",
        "default": """img: '/'"""})

services.register("redirect",
        redirect,
        {"desc": "redirects page to new url. ex: url: /admin/",
        "url": "/admin/",
        "default": "url: '/'",
        "clean": clean_redirect,
        "return": True})

services.register("pages",
        get_pages,
        {"desc": "gets contento pages on given criteria.",
        "default": """filter: services__variables__contains: 'cat: blog'""",
        "clean": clean_page})
