from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ActualiteSitemap, ProjectSitemap, StaticViewSitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "actualites": ActualiteSitemap,
}

urlpatterns = [
    path("", home, name="home"),
    path("mon-espace/", mon_espace, name="mon_espace"),
    path("connexion/", connexion, name="login"),
    path("deconnexion/", deconnexion, name="logout"),
    path("inscription/", register, name="register"),
    path("contact/", contact, name="contact"),
    path("alertes/", alertes, name="alertes"),
    path("alertes/<slug:slug>/", alerte_detail, name="alerte_detail"),
    path("about/", about, name="about"),
    path("historique/", historique, name="historique"),
    path("vision-mission/", vision_mission, name="vision_mission"),
    path("ambition-valeurs/", ambition_valeurs, name="ambition_valeurs"),
    path("equipe-dirigeante/", equipe_dirigeante, name="equipe_dirigeante"),
    path("activite/", activite, name="activite"),
    path(
        "champ_activité/",
        RedirectView.as_view(pattern_name="activite", permanent=True),
    ),
    path("projects/", projects, name="projects"),
    path("recrutement/", recrutement, name="recrutement"),
    path(
        "recrutement/offre/<slug:slug>/postuler/",
        postuler_offre,
        name="postuler_offre",
    ),
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
