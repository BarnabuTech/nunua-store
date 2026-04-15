from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Determine ALLOWED_HOSTS from environment. Prefer explicit `ALLOWED_HOSTS`
# env (comma-separated) or `DOMAIN`. If neither is provided fall back to
# known Vercel hosts so existing Vercel config remains functional.
_env_allowed = os.getenv('ALLOWED_HOSTS')
_env_domain = os.getenv('DOMAIN')
if _env_allowed:
    ALLOWED_HOSTS = [h.strip() for h in _env_allowed.split(',') if h.strip()]
elif _env_domain:
    ALLOWED_HOSTS = [_env_domain, f'www.{_env_domain}']
else:
    # By default allow the Render hostname if not specified via env vars.
    # scheme prefixes are not allowed in ALLOWED_HOSTS so we strip them.
    ALLOWED_HOSTS = ['nunua-store.onrender.com', 'www.nunua-store.onrender.com']

# CSRF trusted origins: prefer explicit env, else build from ALLOWED_HOSTS
_env_csrf = os.getenv('CSRF_TRUSTED_ORIGINS')
if _env_csrf:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _env_csrf.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []
    for host in ALLOWED_HOSTS:
        if host.startswith('.'):
            # skip wildcard entries for direct origin list
            continue
        CSRF_TRUSTED_ORIGINS.append(f'https://{host}')

DISABLE_SERVER_SIDE_CURSORS = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security hardening
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '60'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS', 'DENY')

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

# Previously the Vercel domain was hard-coded here, but newer
# configuration uses the environment-driven logic above instead.  Keep
# this file minimal to avoid accidental overrides.

# Logging configuration for debugging production issues
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email configuration with fallback
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# allauth email verification - set to optional to prevent 500 errors if email fails
ACCOUNT_EMAIL_VERIFICATION = 'optional'