Contento
========

Simple, extendible CMS writen on Django

Features:
* Multilanguage
* Rich text editor
* Easly extendible

Installing
----------

Add to INSTALLED_APPS in settings.py:
    
    'contento',

Add to 'urlpatterns' (at the end) urls.py:
    
    (r'', include('contento.urls')),
