from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("employment/", employment, name="employment"),
    path("about/", about, name="about"),
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
]
