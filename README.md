Contenta
========
Tired of bloated CMS.
Simple, extendible CMS writen on the top of Django. 

Features:
* Multilanguage
* Rich text editor CKEditor http://ckeditor.com/
* Easly extendible 
* Protected pages only for logged users

Requirements:
* django-yamlfield
 
Optional Requirements:
* sorl-thumbnail
* filebrowser - for CKEditor https://github.com/wardi/django-filebrowser-no-grappelli.git
* textile
* markdown
* docutils - restructeredtext

Installing
----------
Install via pip:

    pip install -e git+https://github.com/k1000/contenta.git#egg=contento

Add to INSTALLED_APPS in settings.py:
    
    'contento',
    'sorl.thumbnail',  # *optional
    'filebrowser',  # *optional for CKEditor

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

To register new custom service add somewhere in your code:

    from contento.services import services
    
    # request arg is obligatory
    # returns dict
    def service(request, data):
        # do something...
        return data
        
    # data arg is obligatory
    # returns str with Error description or None
    def clean_service(data):
        # do something...
        return data
        
    # you can set default values too
    # obligatory args: "service name", "function" 
    services.register("service name", 
        service, # function which returns dict with service
        {"desc": "description of the service",
        "clean": clean_service,  # optional function which checks vaild input of variables
        "return": True,  # optional when when service needs intercepts response and redirects to another url for example
        "default": """default_var1: xxx
    default_var2: 2"""})

Licence
-------
