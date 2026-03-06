from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse
import os
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _


def home(request):
    page = "Home"
    context = {"page": page}
    return render(request, "app/home.html", context)

def champ_activité(request):
    page = "Champ d'activité"
    context = {"page": page}
    return render(request, "app/champ_activité.html", context)


def contact(request):
    page = "Contact"
    context = {"page": page}

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("telephone")
        address = request.POST.get("address")
        message = request.POST.get("message")

        subject = f"Nouveau message de {name}"
        body = (
            f"Nom complet: {name}\n"
            f"Email: {email}\n"
            f"Téléphone: {phone}\n"
            f"Adresse: {address}\n\n"
            f"Message:\n{message}"
        )

        try:
            mail = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,  # ✅ ton mail hostinger
                to=[settings.EMAIL_HOST_USER],  # ✅ destinataire (toi-même)
                reply_to=[email],  # ✅ pour pouvoir répondre au visiteur
            )
            mail.send(fail_silently=False)

            messages.success(
                request,
                "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !",
            )
            return HttpResponseRedirect("/contact/")

        except Exception as e:
            messages.error(
                request,
                f"Une erreur est survenue lors de l'envoi du message : {e}",
            )
            return HttpResponseRedirect("/contact/")

    return render(request, "app/contact.html", context)


def about(request):
    page = "A propos"
    context = {"page": page}
    return render(request, "app/about.html", context)


def projects(request):
    page = "Projets"
    context = {"page": page}
    return render(request, "app/projects.html", context)


def detail_project_construction(request, project_id):
    projets = {
        1: {
            "nom": _("Site Kibombo"),
            "description": _(
                "La centrale hydroélectrique de Kibombo sur la rivière Inkisi utilise des technologies modernes pour produire une énergie stable et durable. "
                "Le projet soutient le développement local tout en respectant l’environnement.\n\n"
                "Rivière Inkisi – Kongo-Central – Capacité de 240 MW."
            ),
            "image": "images/inkisi.webp",
        },
        2: {
            "nom": _("Site Nondo"),
            "description": _(
                "Le site hydroélectrique de Nondo sur la rivière Luvua, à Tanganyika, développe 1022 MW avec des installations modernes et durables. "
                "Le projet soutient le développement local et valorise le potentiel hydraulique de la région.\n\n"
                "Rivière Luvua – Tanganyika – Capacité de 1022 MW."
            ),
            "image": "images/luvua.webp",
        },
        3: {
            "nom": _("Site Kilwani"),
            "description": _(
                "Le site hydroélectrique de Kilwani sur la rivière Luvua, à Tanganyika, produit 153 MW grâce à des technologies efficaces et respectueuses de l’environnement. "
                "Il contribue également au développement économique et social local.\n\n"
                "Rivière Luvua – Tanganyika – Capacité de 153 MW."
            ),
            "image": "images/luvua.webp",
        },
    }

    projet = projets.get(project_id, None)

    context = {"page": _("Détails du projet"), "projet": projet}
    return render(request, "app/detail_project_construction.html", context)


def galery(request):
    page = "Galerie"
    context = {"page": page}
    return render(request, "app/galerie.html", context)


def robots_txt(request):
    """
    Vue pour servir le fichier robots.txt de manière dynamique.
    Utilise un template Django pour générer le contenu.
    Optimisé pour le référencement SEO.
    """
    from datetime import datetime

    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )
    context = {
        "sitemap_url": sitemap_url,
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    return render(request, "robots.txt", context, content_type="text/plain")


def site_webmanifest(request):
    """
    Vue pour servir le fichier site.webmanifest de manière dynamique
    avec des URLs absolues pour une meilleure indexation Google.
    """
    base_url = request.build_absolute_uri("/")[:-1]  # Enlever le slash final
    context = {
        "base_url": base_url,
    }
    return render(
        request, "site.webmanifest", context, content_type="application/manifest+json"
    )


def browserconfig_xml(request):
    """
    Vue pour servir le fichier browserconfig.xml de manière dynamique
    avec des URLs absolues.
    """
    base_url = request.build_absolute_uri("/")[:-1]  # Enlever le slash final
    context = {
        "base_url": base_url,
    }
    return render(request, "browserconfig.xml", context, content_type="application/xml")

# impplmentation d'un sy