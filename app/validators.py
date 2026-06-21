import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

User = get_user_model()

PDF_MAX_CANDIDATURE_BYTES = 5 * 1024 * 1024
PHONE_PATTERN = re.compile(r"^\+?[0-9]{9,15}$")


def _strip(value):
    return (value or "").strip() if isinstance(value, str) else ""


def validate_contact(name, email, message):
    errors = {}
    name = _strip(name)
    email = _strip(email)
    message = _strip(message)

    if len(name) < 2:
        errors["name"] = _("Veuillez indiquer votre nom (au moins 2 caractères).")
    elif re.search(r"\d", name):
        errors["name"] = _("Le nom ne doit pas contenir de chiffres.")

    if not email:
        errors["email"] = _("Veuillez indiquer votre adresse e-mail.")
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = _("Veuillez saisir une adresse e-mail valide.")

    if len(message) < 10:
        errors["message"] = _("Votre message doit contenir au moins 10 caractères.")

    return errors, {"name": name, "email": email, "message": message}


def validate_login(username, password):
    errors = {}
    username = _strip(username)
    password = _strip(password)

    if not username:
        errors["username"] = _("Veuillez saisir votre adresse e-mail.")
    else:
        try:
            validate_email(username)
        except ValidationError:
            errors["username"] = _("Veuillez saisir une adresse e-mail valide.")

    if not password:
        errors["password"] = _("Veuillez saisir votre mot de passe.")

    return errors, {"username": username.lower(), "password": password}


def validate_register(full_name, email, password1, password2):
    errors = {}
    full_name = _strip(full_name)
    email = _strip(email).lower()

    if len(full_name) < 2:
        errors["full_name"] = _("Veuillez saisir votre nom complet.")

    if not email:
        errors["email"] = _("Veuillez indiquer votre adresse e-mail.")
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = _("Veuillez saisir une adresse e-mail valide.")
        if "email" not in errors and (
            User.objects.filter(username=email).exists()
            or User.objects.filter(email=email).exists()
        ):
            errors["email"] = _("Un compte existe déjà avec cette adresse e-mail.")

    if not password1:
        errors["password1"] = _("Veuillez choisir un mot de passe.")
    else:
        try:
            validate_password(password1)
        except ValidationError as exc:
            errors["password1"] = " ".join(exc.messages)

    if not password2:
        errors["password2"] = _("Veuillez confirmer votre mot de passe.")
    elif password1 and password1 != password2:
        errors["password2"] = _("Les mots de passe ne correspondent pas.")

    return errors, {
        "full_name": full_name,
        "email": email,
        "password1": password1,
        "password2": password2,
    }


def validate_candidature(prenom, nom, telephone, email, lettre_motivation, cv):
    errors = {}
    prenom = _strip(prenom)
    nom = _strip(nom)
    telephone = _strip(telephone)
    email = _strip(email)
    lettre_motivation = _strip(lettre_motivation)

    if len(prenom) < 2:
        errors["prenom"] = _("Veuillez saisir votre prénom (au moins 2 caractères).")
    elif re.search(r"\d", prenom):
        errors["prenom"] = _("Le prénom ne doit pas contenir de chiffres.")

    if len(nom) < 2:
        errors["nom"] = _("Veuillez saisir votre nom (au moins 2 caractères).")

    if not telephone:
        errors["telephone"] = _("Veuillez saisir votre numéro de téléphone.")
    elif not PHONE_PATTERN.match(telephone):
        errors["telephone"] = _(
            "Veuillez entrer un numéro de téléphone valide (9 à 15 chiffres, avec ou sans +)."
        )

    if not email:
        errors["email"] = _("Veuillez indiquer votre adresse e-mail.")
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = _("Veuillez saisir une adresse e-mail valide.")

    if len(lettre_motivation) < 10:
        errors["lettre_motivation"] = _(
            "Votre lettre de motivation doit contenir au moins 10 caractères."
        )

    if cv is None:
        errors["cv"] = _("Veuillez joindre votre CV au format PDF.")
    else:
        if cv.size > PDF_MAX_CANDIDATURE_BYTES:
            errors["cv"] = _("Le fichier ne doit pas dépasser 5 Mo.")
        else:
            name = (cv.name or "").lower()
            content_type = (cv.content_type or "").lower()
            if not name.endswith(".pdf") and content_type != "application/pdf":
                errors["cv"] = _("Le CV doit être au format PDF.")

    return errors, {
        "prenom": prenom,
        "nom": nom,
        "telephone": telephone,
        "email": email,
        "lettre_motivation": lettre_motivation,
        "cv": cv,
    }


def validate_mon_espace_message(message):
    message = _strip(message)
    if len(message) < 10:
        return _("Votre message doit contenir au moins 10 caractères.")
    return None
