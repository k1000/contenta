from django.conf.urls.defaults import *

urlpatterns = patterns('contento.views',
	(r'^json/(?P<url>.*)$', 'render_json'),
    (r'^(?P<url>.*)$', 'render_page'),
)
