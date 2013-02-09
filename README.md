Contenta
========
Tired of bloated CMS.
Simple, powerfull, extendible CMS writen on the top of Django.

Tested with django 1.4.3

Features:
* Unlimited pages in tree hierarchy
* Multilanguage support
* Rich text editor CKEditor http://ckeditor.com/
* Easily extensible through page services
* Protected pages visible only for logged users
* Edit content right on page (only for html renderer when CONTENTA_EVALUATE_CONTENT is disabled)
* Evaluates content which enable aplaying template_tags directly on content

Requirements:
* django-yamlfield
 
Optional Requirements:
* sorl-thumbnail - https://github.com/sorl/sorl-thumbnail
* filebrowser - for CKEditor https://github.com/wardi/django-filebrowser-no-grappelli.git
* textile
* markdown
* docutils - restructeredtext

Installing
----------
Assuming that you got virtualenv (python virtual envirement) created and activated.

Install via pip:

    pip install -e git+https://github.com/k1000/contenta.git#egg=contenta

Add to INSTALLED_APPS in settings.py file:

    'django.contrib.staticfiles',
    'contenta',
    'sorl.thumbnail',  # *optional
    'filebrowser',  # *optional for CKEditor
    'textile', # *optional for rendering markup
    'markdown', # *optional for rendering markup
    'docutils', # *optional for rendering markup
    

Add to 'urlpatterns' (at the end) urls.py file:
    
    (r'', include('contenta.urls')),
    
Create tables etc.:

    ./manage.py syncdb
    
Collect static files to static the directory
    
    ./manage.py collectstatic
    
Configuration
-------------
Optionally in settings.py set:

* CONTENTA_DEFAULT_RENDERER = 1 (html)
* CONTENTA_DEFAULT_TEMPLATE = 'contenta/default.html'
* CONTENTA_EVALUATE_CONTENT = True

Ussage
------

Accepted variables for page template.

Example:
```yaml
img:
    src: http://justforpaws.co.uk//wp-content/uploads/2012/08/CatSitting1.jpg
    by: anonymous
map:
    lat: 12.145943
    lng: -86.263123
    name: 13A Avenida SE, Managua
youtube: _eXO7hrq2AY
iframe: http://news.ycombinator.com/
en: 
    tags: web, web developement
es:
    tags: web, desarrolo web 
```
Variables with prefix of current active language ex: "en" will be set to default.

Extending
---------
You can extend functionality of the page by registering services and then selecting them in admin panel.
You can pass arbitrary additional parameters to the service introducing YAML (http://www.yaml.org/) formatted text in "parameters" field.

To register new custom service add somewhere in your code:
```python
from contenta.services import services

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
    "default": """default_var1: xxx
default_var2: 2"""})
```
TODO
----

* Automaticaly detect markup options

Licence
-------
