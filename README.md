Contento
========
Django FlatPages on Steroids...
Simple, extendible CMS writen on Django. 

Features:
* Multilanguage
* Rich text editor
* Easly extendible

Requirements:
* django-transmeta 
* django-yamlfield

Installing
----------
Install via pip:

    pip install -e git+https://github.com/k1000/contento.git#egg=contento

Add to INSTALLED_APPS in settings.py:
    
    'contento',

Add to 'urlpatterns' (at the end) urls.py:
    
    (r'', include('contento.urls')),
