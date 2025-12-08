from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import datetime


# Sitemap pour les pages statiques
class StaticViewSitemap(Sitemap):
    """
    Sitemap pour les pages statiques du site Twiga Power.
    Configure les priorités, fréquences de changement et dates de modification.
    """
    protocol = "https"

    def items(self):
        """
        Retourne la liste des pages statiques avec leurs configurations.
        Chaque élément est un tuple (nom_url, priorité, changefreq).
        """
        return [
            ("home", 1.0, "weekly"),  # Page d'accueil - priorité maximale
            ("about", 0.9, "monthly"),  # À propos - haute priorité
            ("projects", 0.9, "weekly"),  # Projets - haute priorité, mis à jour régulièrement
            ("galerie", 0.7, "monthly"),  # Galerie - priorité moyenne
            ("contact", 0.8, "yearly"),  # Contact - priorité moyenne, rarement modifié
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
        # Retourne la date actuelle pour toutes les pages
        # Vous pouvez personnaliser cela pour chaque page si nécessaire
        return datetime.now().date()


# Sitemap pour les pages de projets dynamiques
class ProjectSitemap(Sitemap):
    """
    Sitemap pour les pages de détails des projets.
    """
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        """Retourne la liste des IDs de projets."""
        return [1, 2, 3]  # IDs des projets existants

    def location(self, item):
        """Retourne l'URL de la page de projet."""
        return reverse("detail_project", kwargs={"project_id": item})

    def lastmod(self, item):
        """Retourne la date de dernière modification du projet."""
        return datetime.now().date()
