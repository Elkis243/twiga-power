"""
ASGI config for twiga_power project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv(
        "DJANGO_SETTINGS_MODULE",
        "twiga_power.settings.local",
    ),
)

application = get_asgi_application()