from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Offre(models.Model):

    TYPE_CONTRAT_CHOICES = [
        ("CDI", _("CDI")),
        ("CDD", _("CDD")),
        ("STAGE", _("Stage")),
    ]

    STATUT_CHOICES = [
        ("BROUILLON", _("Brouillon")),
        ("PUBLIE", _("Publié")),
        ("EXPIRE", _("Expiré")),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    description = models.TextField()
    lieu = models.CharField(max_length=150)
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES)
    nombre_postes = models.PositiveIntegerField(default=1)
    date_limite = models.DateField()
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="BROUILLON"
    )
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Offre"
        verbose_name_plural = "Offres"

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            # Slug stable d’après le titre en français (URL unique, indépendante de la langue active)
            from django.utils import translation

            with translation.override(settings.LANGUAGE_CODE or "fr"):
                self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


class ProfileRecherche(models.Model):
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description


class Actualite(models.Model):
    """Actualités publiées sous « Alertes » sur le site."""

    titre = models.CharField(_("Titre"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, max_length=280)
    image = models.ImageField(
        _("Image"),
        upload_to="actualites/",
        help_text=_("Image illustrant l’actualité (obligatoire)."),
    )
    resume = models.TextField(
        _("Résumé"),
        help_text=_("Texte court affiché dans la liste des actualités."),
    )
    contenu = models.TextField(
        _("Contenu"),
        help_text=_("Texte complet de l’actualité (retours à la ligne conservés)."),
    )
    date_publication = models.DateField(_("Date de publication"))
    published = models.BooleanField(_("Publié"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_publication", "-created_at"]
        verbose_name = _("Actualité")
        verbose_name_plural = _("Actualités")

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils import translation

            with translation.override(settings.LANGUAGE_CODE or "fr"):
                self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("alerte_detail", kwargs={"slug": self.slug})
