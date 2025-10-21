"""
WSGI config for nunua project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nunua.settings')

application = get_wsgi_application()

# Required for Vercel — alias 'application' as 'app'
app = application