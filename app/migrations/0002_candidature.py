# Generated manually for Candidature model

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Candidature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prenom", models.CharField(max_length=100)),
                ("nom", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("telephone", models.CharField(max_length=50)),
                ("lettre_motivation", models.TextField()),
                ("cv", models.FileField(upload_to="candidatures/cv/%Y/%m/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "offre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidatures",
                        to="app.offre",
                    ),
                ),
            ],
            options={
                "verbose_name": "Candidature",
                "verbose_name_plural": "Candidatures",
                "ordering": ["-created_at"],
            },
        ),
    ]
