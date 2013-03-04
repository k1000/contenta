from django.utils.translation import ugettext_lazy as _
from django.conf import settings

MULTISITE = getattr(settings, "CONTENTA_MULTISITE", False)

# html renderer
DEFAULT_RENDERER = getattr(settings, "CONTENTA_DEFAULT_RENDERER", 1)

HELP_TXT_YAML = _("""YAML formated markup. http://www.yaml.org/. \
  eg: img:
youtube:
iframe:""")

DEFAULT_TEMPLATE = getattr(settings,
        'CONTENTA_DEFAULT_TEMPLATE',
        'contenta/default.html')

FILEBROWSER_URL = getattr(settings, "CONTENTA_FILEBROWSER_URL",
		"filebrowser/js/FB_CKEditor.js")
