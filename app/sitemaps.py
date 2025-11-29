from django.contrib.sitemaps import Sitemap
from django.urls import reverse


# Sitemap pour les pages statiques
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["home", "contact", "about", "projects", "galerie"]

    def location(self, item):
        return reverse(item)
