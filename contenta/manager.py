from django.db import models


class PageManager(models.Manager):
    def active(self, **filters):
        return super(PageManager, self).get_query_set().filter(state=2, **filters)

    def siblings(self, page):  # TODO
        if page.parent:
            return self.active().filter(parent__pk=page.parent.pk)

    def same_template(self, template_name):
        return self.active().filter(template_name__exact=template_name)
