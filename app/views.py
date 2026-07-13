from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .data.activities import ACTIVITIES
from .data.equipe_dirigeante import EQUIPE_DIRIGEANTE_MEMBERS
from .data.partners import PARTNER_LOGOS
from .models import Actualite, Galerie, Offre

GALLERY_ITEMS_PER_PAGE = 6
from .utils.mail import (
    send_candidature_email,
    send_contact_email,
    send_mon_espace_request_email,
)
from .validators import (
    validate_candidature,
    validate_contact,
    validate_login,
    validate_mon_espace_message,
    validate_register,
)

User = get_user_model()


def home(request):
    page = _("Accueil")
    context = {
        "page": page,
        "partner_logos": PARTNER_LOGOS,
    }
    return render(request, "app/home.html", context)


def activite(request):
    page = _("Activités")
    return render(
        request,
        "app/activite.html",
        {
            "page": page,
            "activities": ACTIVITIES,
        },
    )


def contact(request):
    page = _("Contact")
    post_data = {}
    errors = {}

    if request.method == "POST":
        post_data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "message": request.POST.get("message"),
        }
        errors, cleaned = validate_contact(
            post_data["name"], post_data["email"], post_data["message"]
        )
        post_data = cleaned

        if not errors:
            try:
                send_contact_email(
                    name=cleaned["name"],
                    email=cleaned["email"],
                    message=cleaned["message"],
                )
                messages.success(
                    request,
                    _(
                        "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !"
                    ),
                )
                return redirect("contact")
            except Exception as e:
                messages.error(
                    request,
                    _("Une erreur est survenue lors de l'envoi du message : %(error)s")
                    % {"error": e},
                )

    return render(
        request,
        "app/contact.html",
        {"page": page, "post_data": post_data, "errors": errors},
    )


def about(request):
    page = _("Notre histoire")
    context = {"page": page}
    return render(request, "app/about.html", context)


ALERTES_PER_PAGE = 6
AUTRES_ALERTES_SIDEBAR_LIMIT = 4


def alertes(request):
    queryset = Actualite.objects.filter(published=True)
    paginator = Paginator(queryset, ALERTES_PER_PAGE)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        "app/alertes.html",
        {
            "page": _("Alertes"),
            "page_obj": page_obj,
        },
    )


def alerte_detail(request, slug):
    actualite = get_object_or_404(
        Actualite.objects.filter(published=True),
        slug=slug,
    )
    autres_actualites = (
        Actualite.objects.filter(published=True)
        .exclude(pk=actualite.pk)
        .order_by("-date_publication", "-created_at")[:AUTRES_ALERTES_SIDEBAR_LIMIT]
    )
    return render(
        request,
        "app/alerte_detail.html",
        {
            "page": _("Alertes"),
            "actualite": actualite,
            "autres_actualites": autres_actualites,
        },
    )


def historique(request):
    page = _("Historique")
    context = {"page": page}
    return render(request, "app/historique.html", context)


def vision_mission(request):
    page = _("Vision et mission")
    context = {"page": page}
    return render(request, "app/vision_mission.html", context)


def ambition_valeurs(request):
    page = _("Ambition et valeurs")
    context = {"page": page}
    return render(request, "app/ambition_valeurs.html", context)


def equipe_dirigeante(request):
    page = _("Équipe dirigeante")
    context = {
        "page": page,
        "equipe_members": EQUIPE_DIRIGEANTE_MEMBERS,
    }
    return render(request, "app/equipe_dirigeante.html", context)


def projects(request):
    page = _("Projets")
    context = {"page": page}
    return render(request, "app/projects.html", context)


def recrutement(request):
    page = _("Recrutement")
    context = {"page": page}
    try:
        context["offres"] = (
            Offre.objects.filter(
                statut="PUBLIE",
                active=True,
                date_limite__gte=timezone.now().date(),
            )
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
        post_data = {
            "prenom": request.POST.get("prenom"),
            "nom": request.POST.get("nom"),
            "telephone": request.POST.get("telephone"),
            "email": request.POST.get("email"),
            "lettre_motivation": request.POST.get("lettre_motivation"),
        }
        cv = request.FILES.get("cv")
        errors, cleaned = validate_candidature(
            post_data["prenom"],
            post_data["nom"],
            post_data["telephone"],
            post_data["email"],
            post_data["lettre_motivation"],
            cv,
        )
        post_data = {k: v for k, v in cleaned.items() if k != "cv"}

        if not errors:
            try:
                send_candidature_email(
                    offre,
                    prenom=cleaned["prenom"],
                    nom=cleaned["nom"],
                    email=cleaned["email"],
                    telephone=cleaned["telephone"],
                    lettre_motivation=cleaned["lettre_motivation"],
                    cv_fichier=cleaned["cv"],
                )
                messages.success(
                    request, _("Votre candidature a été envoyée avec succès.")
                )
                return HttpResponseRedirect(reverse("postuler_offre", args=[offre.slug]))
            except Exception as e:
                messages.error(
                    request,
                    _("Une erreur est survenue lors de l'envoi : %(error)s")
                    % {"error": e},
                )

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
    gallery_items = Galerie.objects.filter(est_active=True).order_by("-id")
    paginator = Paginator(gallery_items, GALLERY_ITEMS_PER_PAGE)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        "app/galerie.html",
        {
            "page": _("Galerie"),
            "page_obj": page_obj,
        },
    )


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


def connexion(request):
    if request.user.is_authenticated:
        return redirect("home")

    page = _("Connexion")
    post_data = {}
    errors = {}
    non_field_errors = []

    if request.method == "POST":
        post_data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "remember_me": request.POST.get("remember_me"),
        }
        errors, cleaned = validate_login(
            post_data["username"], post_data["password"]
        )
        post_data["username"] = cleaned["username"]

        if not errors:
            user = authenticate(
                request,
                username=cleaned["username"],
                password=cleaned["password"],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if post_data.get("remember_me"):
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    next_url = request.POST.get("next") or request.GET.get("next")
                    if next_url:
                        return redirect(next_url)
                    return redirect("home")
                non_field_errors = [_("Ce compte est inactif.")]
            else:
                non_field_errors = [
                    _(
                        "Adresse e-mail ou mot de passe incorrect. Veuillez réessayer."
                    )
                ]

    return render(
        request,
        "app/login.html",
        {
            "page": page,
            "post_data": post_data,
            "errors": errors,
            "non_field_errors": non_field_errors,
        },
    )


def deconnexion(request):
    logout(request)
    return redirect("home")


MON_ESPACE_SERVICES = [
    {
        "slug": "reclamation",
        "title": _("Demande de réclamation"),
        "email_subject": _("Demande de réclamation"),
        "description": _(
            "Signalez un problème ou une insatisfaction liée à nos services pour un traitement rapide."
        ),
        "media_tone": "reclamation",
        "media_icon": "bi-exclamation-circle",
        "button_label": _("Nouvelle demande de réclamation"),
        "message_label": _("Votre réclamation"),
        "message_placeholder": _("Décrivez le problème ou l'insatisfaction rencontrée…"),
        "submit_label": _("Envoyer la réclamation"),
    },
    {
        "slug": "suggestion",
        "title": _("Suggestion"),
        "email_subject": _("Suggestion"),
        "description": _(
            "Partagez une idée ou une amélioration pour nous aider à mieux vous accompagner."
        ),
        "media_tone": "suggestion",
        "media_icon": "bi-lightbulb",
        "button_label": _("Nouvelle suggestion"),
        "message_label": _("Votre suggestion"),
        "message_placeholder": _("Partagez votre idée ou amélioration…"),
        "submit_label": _("Envoyer la suggestion"),
    },
    {
        "slug": "service",
        "title": _("Demande de service"),
        "email_subject": _("Demande de service"),
        "description": _(
            "Formulez une nouvelle demande d'assistance ou d'intervention auprès de nos équipes."
        ),
        "media_tone": "service",
        "media_icon": "bi-bag",
        "button_label": _("Nouvelle demande de service"),
        "message_label": _("Votre demande"),
        "message_placeholder": _("Précisez le service ou l'intervention souhaitée…"),
        "submit_label": _("Envoyer la demande"),
    },
]


def _get_mon_espace_service(slug):
    return next((s for s in MON_ESPACE_SERVICES if s["slug"] == slug), None)


@login_required
def mon_espace(request):
    page = _("Mon espace")
    display_name = request.user.get_full_name().strip() or request.user.email
    active_service_slug = (request.GET.get("service") or "").strip()
    post_data_by_service = {}
    errors_by_service = {}

    if request.method == "POST":
        posted_slug = (request.POST.get("service") or "").strip()
        message = (request.POST.get("message") or "").strip()
        service = _get_mon_espace_service(posted_slug)
        active_service_slug = posted_slug
        post_data_by_service[posted_slug] = {"message": message}

        if not service:
            messages.error(request, _("Type de demande invalide."))
            return redirect(reverse("mon_espace"))

        message_error = validate_mon_espace_message(message)
        if message_error:
            errors_by_service[posted_slug] = {"message": message_error}
        else:
            email = request.user.email
            if not email:
                messages.error(
                    request, _("Votre compte ne possède pas d'adresse e-mail.")
                )
                return redirect(f"{reverse('mon_espace')}?service={posted_slug}")

            name = request.user.get_full_name().strip() or email
            try:
                send_mon_espace_request_email(
                    request_subject=str(service["email_subject"]),
                    name=name,
                    email=email,
                    message=message,
                    account_email=email,
                )
                messages.success(
                    request,
                    _(
                        "Votre demande a été envoyée avec succès. Nous vous répondrons bientôt !"
                    ),
                )
                return redirect(reverse("mon_espace"))
            except Exception as e:
                messages.error(
                    request,
                    _("Une erreur est survenue lors de l'envoi : %(error)s")
                    % {"error": e},
                )

    services = []
    for service in MON_ESPACE_SERVICES:
        slug = service["slug"]
        services.append(
            {
                **service,
                "field_prefix": f"{slug}-",
                "modal_target": f"#modal-{slug}",
                "post_data": post_data_by_service.get(slug, {}),
                "errors": errors_by_service.get(slug, {}),
            }
        )

    return render(
        request,
        "app/mon_espace.html",
        {
            "page": page,
            "display_name": display_name,
            "services": services,
            "active_service_slug": active_service_slug,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    page = _("Inscription")
    post_data = {}
    errors = {}

    if request.method == "POST":
        post_data = {
            "full_name": request.POST.get("full_name"),
            "email": request.POST.get("email"),
            "password1": request.POST.get("password1"),
            "password2": request.POST.get("password2"),
        }
        errors, cleaned = validate_register(
            post_data["full_name"],
            post_data["email"],
            post_data["password1"],
            post_data["password2"],
        )
        post_data = {k: v for k, v in cleaned.items() if k != "password1"}

        if not errors:
            parts = cleaned["full_name"].split(None, 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""
            User.objects.create_user(
                username=cleaned["email"],
                email=cleaned["email"],
                password=cleaned["password1"],
                first_name=first_name,
                last_name=last_name,
            )
            messages.success(
                request,
                _("Votre compte a été créé. Connectez-vous pour accéder au portail."),
            )
            return redirect(reverse("login"))

    return render(
        request,
        "app/register.html",
        {"page": page, "post_data": post_data, "errors": errors},
    )
