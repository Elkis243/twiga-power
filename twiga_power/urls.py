"""
URL configuration for twiga_power project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.i18n import set_language

from app import error_views

admin.site.site_header = _("Twiga Power — Administration")
admin.site.site_title = _("Twiga Power")
admin.site.index_title = _("Tableau de bord")

urlpatterns = [
    path("admin/", admin.site.urls),
    # Redirection pour favicon.ico
    path(
        "favicon.ico",
        RedirectView.as_view(url="/static/images/favicon/favicon.ico", permanent=True),
    ),
    path("", include("app.urls")),
    path("i18n/set-language/", set_language, name="set_language"),
]

# Configuration des handlers d'erreur personnalisés
handler400 = error_views.handler400
handler403 = error_views.handler403
handler404 = error_views.handler404
handler500 = error_views.handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
