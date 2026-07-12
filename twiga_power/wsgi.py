"""
WSGI config for twiga_power project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv(
        "DJANGO_SETTINGS_MODULE",
        "twiga_power.settings.local",
    ),
)

application = get_wsgi_application()