from django.utils.translation import ugettext_lazy as _

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
    if not "url" in data:
        ValueError
    return HttpResponseRedirect( data.get("url") )

def get_pages(request, data):
    from models import Page
    pages = Page.objects.filter(**data.get("filter"))
    return pages

services = Services()
services.register("enviroment",
        enviroment, 
        {"desc": "Injects variables into the context of the template"})

services.register("redirect",
        redirect,
        {"desc": "Redirects page to new url. ex: url:http//google.com", 
        "url": "/admin/",
        "return": True})

services.register("pages",
        get_pages,
        {"desc": "Get pages on given criteria.", 
        "default": """filter:
  services__variables__contains: 'cat: blog'""",})

