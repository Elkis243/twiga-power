# Colonnes de traduction (modeltranslation). Idempotent : n’ajoute que les colonnes absentes
# (évite « duplicate column » si une ancienne migration les avait déjà créées).

from django.db import migrations, models


def _existing_columns(schema_editor, table: str) -> set[str]:
    with schema_editor.connection.cursor() as cursor:
        return {
            c.name
            for c in schema_editor.connection.introspection.get_table_description(
                cursor, table
            )
        }


def ensure_translation_columns(apps, schema_editor):
    """Crée uniquement les colonnes manquantes (SQLite et autres backends)."""
    connection = schema_editor.connection

    offre_table = connection.introspection.identifier_converter("app_offre")
    prof_table = connection.introspection.identifier_converter("app_profilerecherche")

    offre_cols = _existing_columns(schema_editor, offre_table)
    prof_cols = _existing_columns(schema_editor, prof_table)

    # (nom_colonne, SQL fragment après ADD COLUMN — SQLite compatible)
    offre_adds = [
        ("description_en", "description_en TEXT NULL"),
        ("description_fr", "description_fr TEXT NULL"),
        ("lieu_en", "lieu_en VARCHAR(150) NULL"),
        ("lieu_fr", "lieu_fr VARCHAR(150) NULL"),
        ("titre_en", "titre_en VARCHAR(200) NULL"),
        ("titre_fr", "titre_fr VARCHAR(200) NULL"),
        ("type_contrat_en", "type_contrat_en VARCHAR(20) NULL"),
        ("type_contrat_fr", "type_contrat_fr VARCHAR(20) NULL"),
    ]
    prof_adds = [
        ("description_en", "description_en TEXT NULL"),
        ("description_fr", "description_fr TEXT NULL"),
    ]

    qn = connection.ops.quote_name
    ot = qn(offre_table)
    pt = qn(prof_table)

    with connection.cursor() as cursor:
        for name, sql_fragment in offre_adds:
            if name not in offre_cols:
                cursor.execute(f"ALTER TABLE {ot} ADD COLUMN {sql_fragment}")
        for name, sql_fragment in prof_adds:
            if name not in prof_cols:
                cursor.execute(f"ALTER TABLE {pt} ADD COLUMN {sql_fragment}")

    # Remplir *_fr depuis les champs de base (SQL : le modèle historique n’a pas encore les champs *_fr)
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE {ot} SET
              {qn("titre_fr")} = {qn("titre")}
            WHERE ({qn("titre_fr")} IS NULL OR {qn("titre_fr")} = '')
              AND {qn("titre")} IS NOT NULL AND {qn("titre")} != ''
            """
        )
        cursor.execute(
            f"""
            UPDATE {ot} SET
              {qn("description_fr")} = {qn("description")}
            WHERE ({qn("description_fr")} IS NULL OR {qn("description_fr")} = '')
              AND {qn("description")} IS NOT NULL AND {qn("description")} != ''
            """
        )
        cursor.execute(
            f"""
            UPDATE {ot} SET
              {qn("lieu_fr")} = {qn("lieu")}
            WHERE ({qn("lieu_fr")} IS NULL OR {qn("lieu_fr")} = '')
              AND {qn("lieu")} IS NOT NULL AND {qn("lieu")} != ''
            """
        )
        cursor.execute(
            f"""
            UPDATE {ot} SET
              {qn("type_contrat_fr")} = {qn("type_contrat")}
            WHERE ({qn("type_contrat_fr")} IS NULL OR {qn("type_contrat_fr")} = '')
              AND {qn("type_contrat")} IS NOT NULL AND {qn("type_contrat")} != ''
            """
        )
        cursor.execute(
            f"""
            UPDATE {pt} SET
              {qn("description_fr")} = {qn("description")}
            WHERE ({qn("description_fr")} IS NULL OR {qn("description_fr")} = '')
              AND {qn("description")} IS NOT NULL AND {qn("description")} != ''
            """
        )


def noop_reverse(apps, schema_editor):
    pass


# État Django = même schéma que si AddField avait tout créé (pour les modèles / admin)
_STATE_FIELDS_OFFRE = [
    migrations.AddField(
        model_name="offre",
        name="description_en",
        field=models.TextField(null=True),
    ),
    migrations.AddField(
        model_name="offre",
        name="description_fr",
        field=models.TextField(null=True),
    ),
    migrations.AddField(
        model_name="offre",
        name="lieu_en",
        field=models.CharField(max_length=150, null=True),
    ),
    migrations.AddField(
        model_name="offre",
        name="lieu_fr",
        field=models.CharField(max_length=150, null=True),
    ),
    migrations.AddField(
        model_name="offre",
        name="titre_en",
        field=models.CharField(max_length=200, null=True),
    ),
    migrations.AddField(
        model_name="offre",
        name="titre_fr",
        field=models.CharField(max_length=200, null=True),
    ),
    migrations.AddField(
        model_name="offre",
        name="type_contrat_en",
        field=models.CharField(
            max_length=20,
            choices=[("CDI", "CDI"), ("CDD", "CDD"), ("STAGE", "Stage")],
            null=True,
        ),
    ),
    migrations.AddField(
        model_name="offre",
        name="type_contrat_fr",
        field=models.CharField(
            max_length=20,
            choices=[("CDI", "CDI"), ("CDD", "CDD"), ("STAGE", "Stage")],
            null=True,
        ),
    ),
]

_STATE_FIELDS_PROFIL = [
    migrations.AddField(
        model_name="profilerecherche",
        name="description_en",
        field=models.TextField(null=True),
    ),
    migrations.AddField(
        model_name="profilerecherche",
        name="description_fr",
        field=models.TextField(null=True),
    ),
]


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_delete_candidature"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(ensure_translation_columns, noop_reverse),
            ],
            state_operations=_STATE_FIELDS_OFFRE + _STATE_FIELDS_PROFIL,
        ),
    ]
