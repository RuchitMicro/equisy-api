"""
WSGI config for equisy_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import  os
from    django.core.wsgi import get_wsgi_application
from    equisy_api.settings import DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equisy_api.settings_dev' if DEBUG else 'equisy_api.settings_prod')

application = get_wsgi_application()
