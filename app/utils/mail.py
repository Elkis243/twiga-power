"""Envoi d’e-mails transactionnels (contact, candidatures, etc.)."""

from __future__ import annotations

from django.conf import settings
from django.core.mail import EmailMessage

from ..models import Offre


def send_contact_email(
    *,
    name: str,
    email: str,
    phone: str,
    address: str,
    message: str,
) -> None:
    subject = f"Nouveau message de {name}"
    body = (
        f"Nom complet: {name}\n"
        f"Email: {email}\n"
        f"Téléphone: {phone}\n"
        f"Adresse: {address}\n\n"
        f"Message:\n{message}"
    )
    mail_kwargs = {
        "subject": subject,
        "body": body,
        "from_email": settings.EMAIL_HOST_USER,
        "to": [settings.EMAIL_HOST_USER],
    }
    if email:
        mail_kwargs["reply_to"] = [email]
    mail = EmailMessage(**mail_kwargs)
    mail.send(fail_silently=False)


def send_candidature_email(
    offre: Offre,
    *,
    prenom: str,
    nom: str,
    email: str,
    telephone: str,
    lettre_motivation: str,
    cv_fichier,
) -> None:
    subject = f"Candidature — {offre.titre} — {prenom} {nom}"
    body = (
        f"Offre : {offre.titre}\n"
        f"Identifiant offre : {offre.id} (slug: {offre.slug})\n\n"
        f"Prénom : {prenom}\n"
        f"Nom : {nom}\n"
        f"Email : {email}\n"
        f"Téléphone : {telephone}\n\n"
        f"Lettre de motivation :\n{lettre_motivation}\n"
    )
    mail_kwargs = {
        "subject": subject,
        "body": body,
        "from_email": settings.EMAIL_HOST_USER,
        "to": [settings.EMAIL_HOST_USER],
    }
    if email:
        mail_kwargs["reply_to"] = [email]
    mail = EmailMessage(**mail_kwargs)
    if cv_fichier:
        filename = getattr(cv_fichier, "name", None) or "cv.pdf"
        if not filename.lower().endswith(".pdf"):
            filename = f"{filename}.pdf"
        cv_fichier.seek(0)
        contenu = cv_fichier.read()
        mail.attach(filename, contenu, "application/pdf")
    mail.send(fail_silently=False)
