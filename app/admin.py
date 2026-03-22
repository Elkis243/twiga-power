from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

# Avant TranslationAdmin : l’autodiscover admin s’exécute avant app.ready()
from . import translation  # noqa: F401

from .models import Offre, ProfileRecherche


class ProfileRechercheInline(TranslationTabularInline):
    model = ProfileRecherche
    extra = 0
    min_num = 0


@admin.register(Offre)
class OffreAdmin(TranslationAdmin):
    list_display = (
        "titre",
        "slug",
        "lieu",
        "type_contrat",
        "statut",
        "nombre_postes",
        "date_limite",
        "active",
        "created_at",
    )
    list_filter = (
        "statut",
        "type_contrat",
        "active",
        "lieu",
        ("date_limite", admin.DateFieldListFilter),
        ("created_at", admin.DateFieldListFilter),
    )
    search_fields = (
        "titre",
        "titre_en",
        "slug",
        "lieu",
        "lieu_en",
        "description",
        "description_en",
    )
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "date_limite"
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("titre",)}
    inlines = [ProfileRechercheInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "titre",
                    "slug",
                    "description",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "statut",
                    "active",
                    "date_limite",
                    "nombre_postes",
                )
            },
        ),
        (
            "Contrat & lieu",
            {
                "fields": (
                    "type_contrat",
                    "lieu",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProfileRecherche)
class ProfileRechercheAdmin(TranslationAdmin):
    list_display = ("id", "offre", "apercu_description")
    list_filter = (
        "offre",
        ("offre__statut", admin.ChoicesFieldListFilter),
        ("offre__type_contrat", admin.ChoicesFieldListFilter),
    )
    search_fields = (
        "description",
        "description_en",
        "offre__titre",
        "offre__titre_en",
        "offre__slug",
    )
    autocomplete_fields = ("offre",)
    ordering = ("offre", "id")

    @admin.display(description="Description")
    def apercu_description(self, obj):
        text = (obj.description or "")[:80]
        return f"{text}…" if len(obj.description or "") > 80 else text
