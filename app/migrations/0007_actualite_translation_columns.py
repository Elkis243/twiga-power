# Colonnes modeltranslation pour Actualité (fr/en), idempotent.

from django.db import migrations, models


def _existing_columns(schema_editor, table: str) -> set[str]:
    with schema_editor.connection.cursor() as cursor:
        return {
            c.name
            for c in schema_editor.connection.introspection.get_table_description(
                cursor, table
            )
        }


def ensure_actualite_translation_columns(apps, schema_editor):
    connection = schema_editor.connection
    table = connection.introspection.identifier_converter("app_actualite")
    cols = _existing_columns(schema_editor, table)

    adds = [
        ("titre_fr", "titre_fr VARCHAR(255) NULL"),
        ("titre_en", "titre_en VARCHAR(255) NULL"),
        ("resume_fr", "resume_fr TEXT NULL"),
        ("resume_en", "resume_en TEXT NULL"),
        ("contenu_fr", "contenu_fr TEXT NULL"),
        ("contenu_en", "contenu_en TEXT NULL"),
    ]

    qn = connection.ops.quote_name
    t = qn(table)

    with connection.cursor() as cursor:
        for name, sql_fragment in adds:
            if name not in cols:
                cursor.execute(f"ALTER TABLE {t} ADD COLUMN {sql_fragment}")

    # Remplir *_fr depuis les champs de base
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE {t} SET
              {qn("titre_fr")} = {qn("titre")}
            WHERE ({qn("titre_fr")} IS NULL OR {qn("titre_fr")} = '')
              AND {qn("titre")} IS NOT NULL AND {qn("titre")} != ''
            """
        )
        cursor.execute(
            f"""
            UPDATE {t} SET
              {qn("resume_fr")} = {qn("resume")}
            WHERE ({qn("resume_fr")} IS NULL OR {qn("resume_fr")} = '')
              AND {qn("resume")} IS NOT NULL AND {qn("resume")} != ''
            """
        )
        cursor.execute(
            f"""
            UPDATE {t} SET
              {qn("contenu_fr")} = {qn("contenu")}
            WHERE ({qn("contenu_fr")} IS NULL OR {qn("contenu_fr")} = '')
              AND {qn("contenu")} IS NOT NULL AND {qn("contenu")} != ''
            """
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_actualite"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    ensure_actualite_translation_columns,
                    noop_reverse,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="actualite",
                    name="titre_fr",
                    field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Titre"),
                ),
                migrations.AddField(
                    model_name="actualite",
                    name="titre_en",
                    field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Titre"),
                ),
                migrations.AddField(
                    model_name="actualite",
                    name="resume_fr",
                    field=models.TextField(blank=True, help_text="Texte court affiché dans la liste des actualités.", null=True, verbose_name="Résumé"),
                ),
                migrations.AddField(
                    model_name="actualite",
                    name="resume_en",
                    field=models.TextField(blank=True, help_text="Texte court affiché dans la liste des actualités.", null=True, verbose_name="Résumé"),
                ),
                migrations.AddField(
                    model_name="actualite",
                    name="contenu_fr",
                    field=models.TextField(blank=True, help_text="Texte complet de l’actualité (retours à la ligne conservés).", null=True, verbose_name="Contenu"),
                ),
                migrations.AddField(
                    model_name="actualite",
                    name="contenu_en",
                    field=models.TextField(blank=True, help_text="Texte complet de l’actualité (retours à la ligne conservés).", null=True, verbose_name="Contenu"),
                ),
            ],
        ),
    ]
