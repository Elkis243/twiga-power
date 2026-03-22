from modeltranslation.translator import translator, TranslationOptions
from .models import Offre, ProfileRecherche

class OffreTranslationOptions(TranslationOptions):
    # type_contrat : codes identiques partout — libellés via gettext_lazy dans le modèle
    fields = ("titre", "description", "lieu")

class ProfileRechercheTranslationOptions(TranslationOptions):
    fields = ('description',)

translator.register(Offre, OffreTranslationOptions)
translator.register(ProfileRecherche, ProfileRechercheTranslationOptions)