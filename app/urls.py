from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProjectSitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
}

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("champ_activité/", champ_activité, name="champ_activité"),
    path("projects/", projects, name="projects"),
    path(
        "projet/<int:project_id>/",
        detail_project_construction,
        name="detail_project",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("galerie/", galery, name="galerie"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("site.webmanifest", site_webmanifest, name="site_webmanifest"),
    path("browserconfig.xml", browserconfig_xml, name="browserconfig_xml"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico")),
    ),
]
