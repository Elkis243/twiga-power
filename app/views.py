from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse
import os
from django.http import FileResponse


def home(request):
    page = "Home"
    context = {"page": page}
    return render(request, "app/home.html", context)


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
            "nom": "Site Kibombo",
            "riviere": "Inkisi",
            "ville": "Kongo-Central",
            "capacite": 240,
            "description": "La centrale hydroélectrique de Kibombo sur la rivière Inkisi utilise des technologies modernes pour produire une énergie stable et durable. Le projet soutient le développement local tout en respectant l’environnement.",
            "image": "images/inkisi.webp",
        },
        2: {
            "nom": "Site Nondo",
            "riviere": "Luvua",
            "ville": "Tanganyika",
            "capacite": 1022,
            "description": "Le site hydroélectrique de Nondo sur la rivière Luvua, à Tanganyika, développe 1022 MW avec des installations modernes et durables. Le projet soutient le développement local et valorise le potentiel hydraulique de la région.",
            "image": "images/luvua.webp",
        },
        3: {
            "nom": "Site Kilwani",
            "riviere": "Luvua",
            "ville": "Tanganyika",
            "capacite": 153,
            "description": "Le site hydroélectrique de Kilwani sur la rivière Luvua, à Tanganyika, produit 153 MW grâce à des technologies efficaces et respectueuses de l’environnement. Il contribue également au développement économique et social local.",
            "image": "images/luvua.webp",
        },
    }

    projet = projets.get(project_id, None)

    context = {"page": "Détails du projet", "projet": projet}
    return render(request, "app/detail_project_construction.html", context)


def galery(request):
    page = "Galerie"
    context = {"page": page}
    return render(request, "app/galerie.html", context)


def robots_txt(request):
    """
    Vue pour servir le fichier robots.txt de manière dynamique.
    Utilise un template Django pour générer le contenu.
    """
    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )
    context = {
        "sitemap_url": sitemap_url,
    }
    return render(request, "robots.txt", context, content_type="text/plain")


def favicon_view(request):
    path = os.path.join(settings.BASE_DIR, "static", "images", "favicon.ico")
    return FileResponse(open(path, "rb"), content_type="image/x-icon")
