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
* filebrowser * optional for CKEditor https://github.com/wardi/django-filebrowser-no-grappelli.git

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
You can pass arbitrary additional variables to the service introducing YAML (http://www.yaml.org/) formatted text in "variables" field.

Example of "variables" field:

    img:
      src: https://www.dzogchen.de/Resources/ssi-logo.gif
    youtube: 8CMlxwvjFEU
    en: 
      tags: web, web developement
    es:
      tags: web, desarrolo web 
    
Variables with prefix of current active language ex: "en" will be set to default.

To register new custom service somewhere in your code add:

    from contento.services import services
    
    # request arg is obligatory
    def foo(request, data):
        # do something...
        return data
        
    # you can set default values too
    # obligatory args: "service name", "function"
    services.register("Foo service", foo, "description of the service", """default_var1: xxx
    default_var2: 2""")

Licence
-------
