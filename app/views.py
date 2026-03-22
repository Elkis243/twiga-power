from datetime import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

PDF_MAX_CANDIDATURE_BYTES = 5 * 1024 * 1024

from .models import Offre
from .utils.mail import send_candidature_email, send_contact_email


# Remplacez les URLs par les sites officiels de chaque partenaire.
PARTNER_LOGOS = [
    {
        "src": "images/partner1.png",
        "alt": _("Logo partenaire 1"),
        "url": "https://www.example.com",
    },
    {
        "src": "images/partner2.png",
        "alt": _("Logo partenaire 2"),
        "url": "https://www.example.com",
    },
    {
        "src": "images/partner3.png",
        "alt": _("Logo partenaire 3"),
        "url": "https://www.example.com",
    },
    {
        "src": "images/partner4.png",
        "alt": _("Logo partenaire 4"),
        "url": "https://www.example.com",
    },
    {
        "src": "images/partner5.png",
        "alt": _("Logo partenaire 5"),
        "url": "https://www.example.com",
    },
]


def home(request):
    page = "Home"
    context = {
        "page": page,
        "partner_logos": PARTNER_LOGOS,
    }
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

        try:
            send_contact_email(
                name=name,
                email=email or "",
                phone=phone or "",
                address=address or "",
                message=message or "",
            )
            messages.success(
                request,
                "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !",
            )
            return HttpResponseRedirect("/contact/")

        except Exception as e:
            messages.error(
                request, f"Une erreur est survenue lors de l'envoi du message : {e}"
            )
            return HttpResponseRedirect("/contact/")

    return render(request, "app/contact.html", context)


def about(request):
    page = "Notre histoire"
    context = {"page": page}
    return render(request, "app/about.html", context)


def projects(request):
    page = "Projets"
    context = {"page": page}
    return render(request, "app/projects.html", context)


def recrutement(request):
    page = "Recrutement"
    context = {"page": page}
    try:
        context["offres"] = (
            Offre.objects.filter(
                statut="PUBLIE",
                active=True,
                date_limite__gte=timezone.now().date(),
            )
            .prefetch_related("profilerecherche_set")
            .order_by("-created_at")
        )
    except Exception:
        context["offres"] = []
    return render(request, "app/recrutement.html", context)


def postuler_offre(request, slug):
    offre = get_object_or_404(
        Offre.objects.prefetch_related("profilerecherche_set"),
        slug=slug,
        statut="PUBLIE",
        active=True,
        date_limite__gte=timezone.now().date(),
    )

    page = "Postuler"
    post_data = {}
    errors = {}

    if request.method == "POST":
        prenom = (request.POST.get("prenom") or "").strip()
        nom = (request.POST.get("nom") or "").strip()
        email = (request.POST.get("email") or "").strip()
        telephone = (request.POST.get("telephone") or "").strip()
        lettre_motivation = (request.POST.get("lettre_motivation") or "").strip()
        cv = request.FILES.get("cv")

        post_data = {
            "prenom": prenom,
            "nom": nom,
            "email": email,
            "telephone": telephone,
            "lettre_motivation": lettre_motivation,
        }
        send_candidature_email(
            offre,
            prenom=prenom,
            nom=nom,
            email=email,
            telephone=telephone,
            lettre_motivation=lettre_motivation,
            cv_fichier=cv,
        )
        messages.success(request, _("Votre candidature a été envoyée avec succès."))
        return HttpResponseRedirect(reverse("postuler_offre", args=[offre.slug]))
    return render(
        request,
        "app/postuler_offre.html",
        {
            "page": page,
            "offre": offre,
            "post_data": post_data,
            "errors": errors,
        },
    )


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

    p = projets.get(project_id)
    if not p:
        raise Http404(_("Projet introuvable"))

    desc = p["description"]
    if "\n\n" in desc:
        body, facts_line = desc.rsplit("\n\n", 1)
        body = body.strip()
        facts_line = facts_line.strip()
    else:
        body = desc
        facts_line = ""

    if facts_line:
        if " – " in facts_line:
            fact_items = [x.strip() for x in facts_line.split(" – ")]
        elif " - " in facts_line:
            fact_items = [x.strip() for x in facts_line.split(" - ")]
        else:
            fact_items = [facts_line]
    else:
        fact_items = []

    projet = {
        "nom": p["nom"],
        "image": p["image"],
        "body": body,
        "facts_line": facts_line,
        "fact_items": fact_items,
    }

    context = {"page": p["nom"], "projet": projet}
    return render(request, "app/detail_project_construction.html", context)


def galery(request):
    page = "Galerie"
    context = {"page": page}
    return render(request, "app/galerie.html", context)


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )
    context = {
        "sitemap_url": sitemap_url,
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    return render(request, "robots.txt", context, content_type="text/plain")


def site_webmanifest(request):
    base_url = request.build_absolute_uri("/")[:-1]  # Enlever le slash final
    context = {
        "base_url": base_url,
    }
    return render(
        request, "site.webmanifest", context, content_type="application/manifest+json"
    )


def browserconfig_xml(request):
    base_url = request.build_absolute_uri("/")[:-1]  # Enlever le slash final
    context = {
        "base_url": base_url,
    }
    return render(request, "browserconfig.xml", context, content_type="application/xml")
