# Suppression du modèle Candidature (envoi e-mail uniquement, sans BDD)

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_candidature"),
    ]

    operations = [
        migrations.DeleteModel(name="Candidature"),
    ]
