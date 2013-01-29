from django.conf.urls.defaults import patterns

urlpatterns = patterns('contenta.views',
	(r'^json/(?P<url>.*)$', 'render_json'),
	(r'^save(?P<url>.*)$', 'save_content'),
    (r'^(?P<url>.*)$', 'render_page'),
)
