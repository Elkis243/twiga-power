from .base import *

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = ['www.twigapower.com', 'twigapower.com']

SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS') == 'True'
SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD') == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT') == 'True'

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE') == 'True'
CSRF_TRUSTED_ORIGINS = ['https://twigapower.com']

X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS')
SECURE_BROWSER_XSS_FILTER = os.getenv('SECURE_BROWSER_XSS_FILTER') == 'True'
SECURE_CONTENT_TYPE_NOSNIFF = os.getenv('SECURE_CONTENT_TYPE_NOSNIFF') == 'True'