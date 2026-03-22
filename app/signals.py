"""
Traduction automatique FR → EN à l’enregistrement (champs *_en vides uniquement).
"""

from __future__ import annotations

import logging

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import translation

from .models import Offre, ProfileRecherche

logger = logging.getLogger(__name__)


def _is_empty_en(value) -> bool:
    return value is None or (isinstance(value, str) and not str(value).strip())


def _fill_offre_en_from_fr(instance: Offre) -> None:
    from .utils.auto_translate import translate_fr_to_en

    with translation.override("fr"):
        titre_fr = (instance.titre or "").strip()
        desc_fr = (instance.description or "").strip()
        lieu_fr = (instance.lieu or "").strip()

    if titre_fr and _is_empty_en(getattr(instance, "titre_en", None)):
        instance.titre_en = translate_fr_to_en(titre_fr)
    if desc_fr and _is_empty_en(getattr(instance, "description_en", None)):
        instance.description_en = translate_fr_to_en(desc_fr)
    if lieu_fr and _is_empty_en(getattr(instance, "lieu_en", None)):
        instance.lieu_en = translate_fr_to_en(lieu_fr)


@receiver(pre_save, sender=Offre)
def auto_translate_offre(sender, instance: Offre, **kwargs):
    if not getattr(settings, "AUTO_TRANSLATE_ENABLED", True):
        return
    try:
        _fill_offre_en_from_fr(instance)
    except Exception as exc:
        logger.warning("Traduction auto Offre id=%s : %s", getattr(instance, "pk", None), exc)


@receiver(pre_save, sender=ProfileRecherche)
def auto_translate_profil_recherche(sender, instance: ProfileRecherche, **kwargs):
    if not getattr(settings, "AUTO_TRANSLATE_ENABLED", True):
        return
    try:
        from .utils.auto_translate import translate_fr_to_en

        with translation.override("fr"):
            src = (instance.description or "").strip()
        if src and _is_empty_en(getattr(instance, "description_en", None)):
            instance.description_en = translate_fr_to_en(src)
    except Exception as exc:
        logger.warning(
            "Traduction auto ProfileRecherche id=%s : %s",
            getattr(instance, "pk", None),
            exc,
        )
