# Modèle Actualité (colonnes modeltranslation ajoutées par `makemigrations` après déploiement).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_remove_offre_type_contrat_translation_columns"),
    ]

    operations = [
        migrations.CreateModel(
            name="Actualite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titre", models.CharField(max_length=255, verbose_name="Titre")),
                ("slug", models.SlugField(blank=True, max_length=280, unique=True, verbose_name="Slug")),
                (
                    "resume",
                    models.TextField(help_text="Texte court affiché dans la liste des actualités.", verbose_name="Résumé"),
                ),
                (
                    "contenu",
                    models.TextField(help_text="Texte complet de l’actualité (retours à la ligne conservés).", verbose_name="Contenu"),
                ),
                ("date_publication", models.DateField(verbose_name="Date de publication")),
                ("published", models.BooleanField(default=False, verbose_name="Publié")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Actualité",
                "verbose_name_plural": "Actualités",
                "ordering": ["-date_publication", "-created_at"],
            },
        ),
    ]
