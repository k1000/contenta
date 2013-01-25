Contento
========
Django FlatPages on Steroids...
Simple, extendible CMS writen on Django. 

Features:
* Multilanguage
* Rich text editor CKEditor http://ckeditor.com/
* Easly extendible

Requirements:
* django-transmeta 
* django-yamlfield
* sorl-thumbnail *optional

Installing
----------
Install via pip:

    pip install -e git+https://github.com/k1000/contento.git#egg=contento

Add to INSTALLED_APPS in settings.py:
    
    'contento',
    'sorl.thumbnail',  # *optional

Add to 'urlpatterns' (at the end) urls.py:
    
    (r'', include('contento.urls')),
    
Create tables etc.:

    python manage.py syncdb

Extending
---------
You can extend functionality of the page by registering services and then selecting them in admin panel.
You can pass additional variables to the service introducing YAML (http://www.yaml.org/) formatted text in "variables" field.

Somewhere in your code add:

    from contento.views import services
    
    # request arg is obligatory
    def foo(request, data):
        # do something...
        return data
    services.register("Foo service", foo, "description of the service")

Licence
-------
