"""
Traduction FR → EN (Google via deep-translator), utilisée par les signaux et l’admin.
"""

from __future__ import annotations

from django.conf import settings


def translate_fr_to_en(text: str) -> str:
    if text is None:
        return ""
    text = str(text).strip()
    if not text:
        return ""

    if not getattr(settings, "AUTO_TRANSLATE_ENABLED", True):
        raise RuntimeError("AUTO_TRANSLATE_ENABLED est désactivé.")

    try:
        from deep_translator import GoogleTranslator
    except ImportError as e:
        raise RuntimeError("Installez : pip install deep-translator") from e

    return GoogleTranslator(source="fr", target="en").translate(text)
