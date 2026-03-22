from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        super().ready()
        from . import translation  # noqa: F401 — enregistrement modeltranslation

        # Signaux (traduction auto) après modeltranslation
        from . import signals  # noqa: F401
