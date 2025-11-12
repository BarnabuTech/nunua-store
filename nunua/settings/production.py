from .base import *
# import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.vercel.app']

# Get allowed hosts from environment variable or use wildcard for Vercel
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'nunua-store-website.vercel.app').split(',')

# CSRF_TRUSTED_ORIGINS for production
# CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS]

DISABLE_SERVER_SIDE_CURSORS = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_PRELOAD = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', ''),
        'USER': os.getenv('DATABASE_USER', ''),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'HOST': os.getenv('DATABASE_HOST', ''),
        'PORT': os.getenv('DATABASE_PORT', '5432'),  # Default to 5432 if not provided
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECK': True,
        'OPTIONS': {
            'sslmode':'require',
            'client_encoding': 'UTF8'
        }
    }
}

# Static files are handled by Whitenoise in Vercel
# No need for additional static file serving in production

# The Domain URL of Vercel deployment
DOMAIN = "https://nunua-store-website.vercel.app"
CSRF_TRUSTED_ORIGINS = ['https://nunua-store-website.vercel.app']

# Get domain from environment variable
# DOMAIN = os.getenv('DOMAIN', '')
# CSRF_TRUSTED_ORIGINS.extend([f'https://{DOMAIN}', f'https://www.{DOMAIN}'] if DOMAIN else [])