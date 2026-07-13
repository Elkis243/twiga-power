from .base import *

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [
    "twiga-power-production.up.railway.app",
    "twigapower.com",
    "www.twigapower.com",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS') == 'True'
SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD') == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT') == 'True'

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE') == 'True'
CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
    "https://twigapower.com",
    "https://www.twigapower.com",
]

X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS')
SECURE_BROWSER_XSS_FILTER = os.getenv('SECURE_BROWSER_XSS_FILTER') == 'True'
SECURE_CONTENT_TYPE_NOSNIFF = os.getenv('SECURE_CONTENT_TYPE_NOSNIFF') == 'True'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}