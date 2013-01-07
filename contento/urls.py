from django.conf.urls.defaults import *

urlpatterns = patterns('contento.views',
    (r'^(?P<url>.*)$', 'page'),
)
