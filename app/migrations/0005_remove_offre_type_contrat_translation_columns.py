# type_contrat : même code métier (CDI/CDD/STAGE) pour toutes les langues —
# les libellés passent par gettext_lazy, pas par des colonnes *_en/_fr.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_offre_description_en_offre_description_fr_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="offre",
            name="type_contrat_en",
        ),
        migrations.RemoveField(
            model_name="offre",
            name="type_contrat_fr",
        ),
    ]
