from .base import *

# Development-specific settings
DEBUG = False  # Set to False to test production-like behavior in development 

# Override ALLOWED_HOSTS for development
ALLOWED_HOSTS = ['nunua-store.onrender.com', 'localhost', '127.0.0.1']

# Override CSRF_TRUSTED_ORIGINS for development
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

SECURE_SSL_REDIRECT = False

# Database for development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'