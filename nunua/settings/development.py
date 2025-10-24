from .base import *

# Development-specific settings
DEBUG = False

# Override ALLOWED_HOSTS for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Override CSRF_TRUSTED_ORIGINS for development
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

# Database for development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'