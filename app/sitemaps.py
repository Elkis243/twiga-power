from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime, timedelta
from django.conf import settings


# Sitemap pour les pages statiques
class StaticViewSitemap(Sitemap):
    """
    Sitemap pour les pages statiques du site Twiga Power.
    Configure les priorités, fréquences de changement et dates de modification.
    Optimisé pour le référencement SEO.
    """

    protocol = "https"
    limit = 5000  # Limite maximale d'URLs par sitemap

    def items(self):
        """
        Retourne la liste des pages statiques avec leurs configurations.
        Chaque élément est un tuple (nom_url, priorité, changefreq, lastmod_days).
        """
        return [
            (
                "home",
                1.0,
                "daily",
                0,
            ),  # Page d'accueil - priorité maximale, mise à jour quotidienne
            ("about", 0.9, "monthly", 30),  # À propos - haute priorité
            (
                "projects",
                0.9,
                "weekly",
                7,
            ),  # Projets - haute priorité, mis à jour régulièrement
            (
                "galerie",
                0.8,
                "weekly",
                14,
            ),  # Galerie - priorité élevée, mise à jour hebdomadaire
            (
                "contact",
                0.7,
                "yearly",
                365,
            ),  # Contact - priorité moyenne, rarement modifié
        ]

    def location(self, item):
        """Retourne l'URL de la page."""
        return reverse(item[0])

    def priority(self, item):
        """Retourne la priorité de la page (0.0 à 1.0)."""
        return item[1]

    def changefreq(self, item):
        """Retourne la fréquence de changement de la page."""
        return item[2]

    def lastmod(self, item):
        """Retourne la date de dernière modification."""
        # Calcule la date en fonction du nombre de jours depuis la dernière modification
        days_ago = item[3]
        return (datetime.now() - timedelta(days=days_ago)).date()


# Sitemap pour les pages de projets dynamiques
class ProjectSitemap(Sitemap):
    """
    Sitemap pour les pages de détails des projets.
    Inclut les images pour améliorer le référencement visuel.
    """

    changefreq = "monthly"
    priority = 0.85
    protocol = "https"
    limit = 5000

    # Données des projets avec leurs images
    PROJETS_DATA = {
        1: {
            "nom": "Site Kibombo",
            "image": "images/inkisi.webp",
            "lastmod_days": 15,
        },
        2: {
            "nom": "Site Nondo",
            "image": "images/luvua.webp",
            "lastmod_days": 10,
        },
        3: {
            "nom": "Site Kilwani",
            "image": "images/luvua.webp",
            "lastmod_days": 20,
        },
    }

    def items(self):
        """Retourne la liste des IDs de projets."""
        return list(self.PROJETS_DATA.keys())

    def location(self, item):
        """Retourne l'URL de la page de projet."""
        return reverse("detail_project", kwargs={"project_id": item})

    def lastmod(self, item):
        """Retourne la date de dernière modification du projet."""
        projet_data = self.PROJETS_DATA.get(item, {})
        days_ago = projet_data.get("lastmod_days", 30)
        return (datetime.now() - timedelta(days=days_ago)).date()

    def images(self, item):
        """
        Retourne les images associées au projet pour le sitemap.
        Améliore le référencement des images dans Google Images.
        Django convertira automatiquement les URLs relatives en URLs absolues.
        """
        projet_data = self.PROJETS_DATA.get(item, {})
        image_path = projet_data.get("image", "")

        if not image_path:
            return []

        # Utiliser une URL relative - Django la convertira en URL absolue automatiquement
        # lors de la génération du sitemap
        image_url = f"/static/{image_path}"
        projet_nom = projet_data.get("nom", f"Projet {item}")

        return [
            {
                "loc": image_url,
                "title": f"{projet_nom} - Twiga Power",
                "caption": f"Centrale hydroélectrique {projet_nom} - Production d'énergie renouvelable",
                "geo_location": "République Démocratique du Congo",
            }
        ]
