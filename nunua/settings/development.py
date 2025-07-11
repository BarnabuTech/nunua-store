from .base import *

# Development-specific settings
DEBUG = True

# Add 'localhost' to ALLOWED_HOSTS for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DOMAINS = ['localhost', '127.0.0.1']
SECURE_SSL_REDIRECT = False
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'