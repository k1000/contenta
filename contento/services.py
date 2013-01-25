from django.utils.translation import ugettext_lazy as _

class Services():
    services = list()

    def register(self, name, service, description="", defaults="", **kwargs):
        self.services.append([name, service, description, defaults, kwargs])

    def unregister(self, name):
        del(self.services[name])

    def list(self):
        return [[i, ser[0]] for i, ser in enumerate(self.services)]

    def get(self, index):
        return self.services[int(index)]

# very simple service just takes variables from input and injects them to the template
def enviroment(request, data):
    return data

services = Services()
services.register(_("enviroment"), enviroment, "Injects variables into the context of the template")