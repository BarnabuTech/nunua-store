import os

settings_module = os.getenv('DJANGO_SETTINGS_MODULE')

if settings_module == 'nunua.settings.production':
    from .production import *
else:
    from .development import *