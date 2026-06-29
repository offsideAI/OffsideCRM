"""
WSGI config for uderzoai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uderzoai.settings')

application = get_wsgi_application()

if os.getenv('DJANGO_SETTINGS_MODULE'):
    for key, value in os.environ.items():
        print(f"{key}: {value}")