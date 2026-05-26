# Si la migration échoue (actualités sans image), supprimez ou complétez les lignes
# dans l’admin avant d’appliquer, ou videz la table app_actualite en dev.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_actualite_translation_columns"),
    ]

    operations = [
        migrations.AddField(
            model_name="actualite",
            name="image",
            field=models.ImageField(
                help_text="Image illustrant l’actualité (obligatoire).",
                upload_to="actualites/",
                verbose_name="Image",
            ),
        ),
    ]
